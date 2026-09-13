# =====================================================================
# DEMO 3 — ONE file, N datasets: the metadata-driven pipeline
# =====================================================================
# HOW IT WORKS:
#   1. At update start, this file is evaluated top-to-bottom.
#   2. We read the CONFIG TABLE with plain spark.read (allowed at
#      graph-evaluation time) and loop over its active rows.
#   3. For each row we EMIT datasets via factory functions:
#        - bronze_<entity>_dyn                (always; Auto Loader ST)
#        - load_type = append -> silver_<entity>_dyn (expectations from config)
#        - load_type = scd1/scd2 -> silver_<entity>_dyn via AUTO CDC
#   4. Add a config row -> next update grows the graph. No code change.
#
# CLASSIC PITFALL shown on purpose: Python closures in a loop capture the
# VARIABLE, not the value — hence the `cfg=cfg` default-argument trick and
# explicit `name=` on every decorator.
# =====================================================================

from pyspark import pipelines as dp
from pyspark.sql import functions as F

SOURCE_PATH = spark.conf.get("source_path")
CONFIG_TABLE = spark.conf.get("config_table")

# Graph-evaluation-time read: config rows become plain Python dicts.
config_rows = [
    r.asDict() for r in spark.read.table(CONFIG_TABLE)
    .where("active = true")
    .collect()
]
assert config_rows, f"No active rows in {CONFIG_TABLE} — nothing to build."


def make_bronze(cfg):
    """Factory: one Auto Loader streaming table per config row."""
    entity = cfg["entity"]

    @dp.table(
        name=f"bronze_{entity}_dyn",
        comment=f"[metadata-driven] raw '{entity}' from {cfg['source_subdir']} ({cfg['source_format']})",
        table_properties={"quality": "bronze", "source_entity": entity},
    )
    def _bronze(cfg=cfg):  # default arg pins THIS row's values
        reader = (
            spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", cfg["source_format"])
            .option("cloudFiles.inferColumnTypes", "true")
        )
        if cfg["source_format"] == "csv":
            reader = reader.option("header", "true")
        return (
            reader.load(f"{SOURCE_PATH}/{cfg['source_subdir']}")
            .withColumn("_ingest_ts", F.col("_metadata.file_modification_time"))
            .withColumn("_ingest_file", F.col("_metadata.file_name"))
        )


def make_silver_append(cfg):
    """Factory: expectations-gated silver for append entities."""
    entity = cfg["entity"]
    rules = dict(cfg["expectations"] or {})

    @dp.table(
        name=f"silver_{entity}_dyn",
        comment=f"[metadata-driven] validated '{entity}' (rules from config)",
        table_properties={"quality": "silver"},
    )
    @dp.expect_all_or_drop(rules)
    def _silver(entity=entity):
        return spark.readStream.table(f"bronze_{entity}_dyn")


def make_silver_scd(cfg):
    """Factory: AUTO CDC silver (SCD1 or SCD2) driven by config."""
    entity = cfg["entity"]
    scd_type = 1 if cfg["load_type"] == "scd1" else 2

    dp.create_streaming_table(
        name=f"silver_{entity}_dyn",
        comment=f"[metadata-driven] '{entity}' as SCD{scd_type} (keys/sequence from config)",
        expect_all_or_drop=dict(cfg["expectations"] or {}),
    )
    dp.create_auto_cdc_flow(
        target=f"silver_{entity}_dyn",
        source=f"bronze_{entity}_dyn",
        keys=list(cfg["primary_keys"]),
        sequence_by=cfg["sequence_col"],
        stored_as_scd_type=scd_type,
        except_column_list=["_ingest_ts", "_ingest_file", "_rescued_data"],
    )


# --- The loop that builds the whole graph ----------------------------
for cfg in config_rows:
    make_bronze(cfg)
    if cfg["load_type"] == "append":
        make_silver_append(cfg)
    elif cfg["load_type"] in ("scd1", "scd2"):
        make_silver_scd(cfg)
    else:
        raise ValueError(f"Unknown load_type '{cfg['load_type']}' for entity '{cfg['entity']}'")

# TALKING POINTS:
#   - This is how ingestion FRAMEWORKS are built (50-500 tables, one file).
#   - Config is data: governed, permissioned, auditable in Unity Catalog.
#   - Caveats: config read at update START; validate rows (see the raise
#     above) or a typo becomes a runtime surprise; keep it simple for
#     small pipelines — plain code beats a framework for 5 tables.
