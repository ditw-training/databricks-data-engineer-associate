# =====================================================================
# STAGE 2 — SILVER: AUTO CDC — SCD Type 1 vs SCD Type 2, side by side
# =====================================================================
# DEMO SCRIPT:
#   - The CDC "feed" is the customers landing folder: first the full
#     snapshot (customers_000_initial.csv), later a change file
#     (customers_001_changes.csv: 14 rows = 7 changed + 6 new customers + 1 unchanged).
#   - sequence_by = file modification time -> AUTO CDC orders events and
#     handles late/duplicate events per key.
#   - ONE source feeds TWO targets:
#       * silver_customers_scd1 -> latest value wins, no history
#       * silver_customers_scd2 -> history kept via __START_AT / __END_AT
#   - `dp.create_auto_cdc_flow` / SQL `AUTO CDC INTO` are the current API; older
#     material shows the legacy names `dlt.apply_changes` / `APPLY CHANGES INTO`.
# =====================================================================

from pyspark import pipelines as dp
from pyspark.sql import functions as F

SOURCE_PATH = spark.conf.get("source_path")


# --- 2a. Append-only CDC feed (bronze) ------------------------------
@dp.table(
    name="bronze_customers_cdc",
    comment="Append-only customer snapshots/changes; the AUTO CDC source.",
)
def bronze_customers_cdc():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("header", "true")
        .load(f"{SOURCE_PATH}/customers")
        .withColumn("_event_ts", F.col("_metadata.file_modification_time"))
    )


# --- 2b. SCD TYPE 1 — overwrite in place ----------------------------
dp.create_streaming_table(
    name="silver_customers_scd1",
    comment="Current-state customers (SCD1): updates overwrite, no history.",
)

dp.create_auto_cdc_flow(
    target="silver_customers_scd1",
    source="bronze_customers_cdc",
    keys=["customer_id"],
    sequence_by="_event_ts",
    stored_as_scd_type=1,
    except_column_list=["_event_ts", "_rescued_data"],
)


# --- 2c. SCD TYPE 2 — full history ----------------------------------
dp.create_streaming_table(
    name="silver_customers_scd2",
    comment="Historized customers (SCD2): __START_AT/__END_AT track validity.",
)

dp.create_auto_cdc_flow(
    target="silver_customers_scd2",
    source="bronze_customers_cdc",
    keys=["customer_id"],
    sequence_by="_event_ts",
    stored_as_scd_type=2,
    except_column_list=["_event_ts", "_rescued_data"],
)

# TALKING POINTS:
#   - SCD1 answers "what is true NOW" (operational lookups).
#   - SCD2 answers "what was true WHEN" (point-in-time analytics, audits).
#   - Current row in SCD2: WHERE __END_AT IS NULL.
#   - Deletes: feed a delete flag and pass apply_as_deletes=... (not used here).
