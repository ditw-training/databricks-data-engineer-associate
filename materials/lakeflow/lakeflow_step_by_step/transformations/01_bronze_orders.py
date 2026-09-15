# =====================================================================
# STAGE 1 — BRONZE: incremental file ingestion with a streaming table
# =====================================================================
# DEMO SCRIPT:
#   1st pipeline run  -> ingests every file already in <source_path>/orders
#   2nd run, no files -> 0 rows processed. WHY? Every streaming flow owns a
#                        CHECKPOINT (stored in pipeline-managed storage) that
#                        records which files/offsets were already consumed.
#   after wave 2 drop -> ONLY the new files are read. That is the whole point
#                        of a STREAMING TABLE: incremental, exactly-once.
#   Full refresh      -> resets the checkpoint and rebuilds from all files.
#
# `read_files` under streaming = Auto Loader (cloudFiles) semantics:
# file discovery + schema inference + rescued data, managed for you.
# =====================================================================

from pyspark import pipelines as dp
from pyspark.sql import functions as F

SOURCE_PATH = spark.conf.get("source_path")  # set in pipeline Configuration


@dp.table(
    name="bronze_orders_sdp",
    comment="Raw orders, ingested incrementally from JSON files (Auto Loader).",
    table_properties={"quality": "bronze"},
)
def bronze_orders_sdp():
    return (
        spark.readStream.format("cloudFiles")               # Auto Loader
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(f"{SOURCE_PATH}/orders")
        # Ingestion metadata — provenance columns are a bronze best practice:
        .select(
            "*",
            F.col("_metadata.file_name").alias("_ingest_file"),
            F.col("_metadata.file_modification_time").alias("_ingest_ts"),
        )
    )

# SQL equivalent (show on screen, don't add both — same dataset name!):
#
#   CREATE OR REFRESH STREAMING TABLE bronze_orders_sdp
#   COMMENT 'Raw orders, ingested incrementally from JSON files.'
#   AS SELECT *,
#          _metadata.file_name              AS _ingest_file,
#          _metadata.file_modification_time AS _ingest_ts
#   FROM STREAM read_files('${source_path}/orders', format => 'json');
