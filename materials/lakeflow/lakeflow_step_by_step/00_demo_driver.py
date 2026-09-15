# Databricks notebook source
# MAGIC %md
# MAGIC # DEMO 1 Driver — Lakeflow SDP step by step
# MAGIC
# MAGIC 👨‍🏫 **TRAINER notebook** — run these cells *between* pipeline updates. It is **not** part of the pipeline source.
# MAGIC
# MAGIC Follow the step numbers from `README.md`.

# COMMAND ----------

# MAGIC %run ../../../notebooks/setup/00_setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1 — Prepare landing folders + wave 1
# MAGIC Creates `landing_sdp/{orders,customers}` in your bronze Volume and copies the FIRST wave of files.

# COMMAND ----------

LANDING = f"/Volumes/{CATALOG}/{BRONZE_SCHEMA}/landing_sdp"
ORDERS_LANDING = f"{LANDING}/orders"
CUSTOMERS_LANDING = f"{LANDING}/customers"

spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{BRONZE_SCHEMA}.landing_sdp")
for d in (ORDERS_LANDING, CUSTOMERS_LANDING):
    dbutils.fs.mkdirs(d)

# Wave 1: first stream file + the initial customers snapshot
dbutils.fs.cp(f"{DATASET_PATH}/orders/stream/orders_stream_001.json", f"{ORDERS_LANDING}/orders_stream_001.json")
dbutils.fs.cp(f"{DATASET_PATH}/customers/customers.csv", f"{CUSTOMERS_LANDING}/customers_000_initial.csv")

print("Pipeline configuration value to set:")
print(f"  source_path = {LANDING}")
print("\nLanded files:")
display(dbutils.fs.ls(ORDERS_LANDING) + dbutils.fs.ls(CUSTOMERS_LANDING))

# COMMAND ----------

# MAGIC %md
# MAGIC ➡️ Now **run the pipeline** (only `01_bronze_orders.py` active). Then run it a SECOND time with no new files:
# MAGIC the update reports **0 rows** — the flow's **checkpoint** (managed by the pipeline) remembers which files were already ingested.
# MAGIC A *full refresh* resets that checkpoint and rebuilds the table from all files.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2 — Drop wave 2 (incremental ingestion proof)

# COMMAND ----------

dbutils.fs.cp(f"{DATASET_PATH}/orders/stream/orders_stream_002.json", f"{ORDERS_LANDING}/orders_stream_002.json")
dbutils.fs.cp(f"{DATASET_PATH}/orders/stream/orders_stream_003.json", f"{ORDERS_LANDING}/orders_stream_003.json")
print("Wave 2 landed (2 files, 20k rows). Run the pipeline — ONLY these rows will be processed.")

# COMMAND ----------

# Verify after the pipeline update:
display(spark.sql(f"""
    SELECT _ingest_file, COUNT(*) AS rows
    FROM {CATALOG}.sdp_demo.bronze_orders_sdp
    GROUP BY _ingest_file ORDER BY _ingest_file
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3 — CDC feed: changed customers
# MAGIC `customers_new.csv` has 14 rows: 7 existing customers with CHANGED attributes (e.g. `CUST000001` moved New York → Seattle), 6 new customers and 1 unchanged row.
# MAGIC The file's modification time becomes the CDC **sequence** — AUTO CDC orders events by it.

# COMMAND ----------

dbutils.fs.cp(f"{DATASET_PATH}/customers/customers_new.csv", f"{CUSTOMERS_LANDING}/customers_001_changes.csv")
print("Changes landed. Run the pipeline (with 02_silver_customers_scd.py active).")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4 — SCD1 vs SCD2, side by side

# COMMAND ----------

print("SCD TYPE 1 — attribute overwritten in place, no history:")
display(spark.sql(f"""
    SELECT customer_id, first_name, city, customer_segment
    FROM {CATALOG}.sdp_demo.silver_customers_scd1 WHERE customer_id = 'CUST000001'
"""))

print("SCD TYPE 2 — full history: old row closed (__END_AT), current row open (__END_AT IS NULL):")
display(spark.sql(f"""
    SELECT customer_id, city, `__START_AT`, `__END_AT`
    FROM {CATALOG}.sdp_demo.silver_customers_scd2
    WHERE customer_id = 'CUST000001' ORDER BY `__START_AT`
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5 — Event log: expectations & flow metrics
# MAGIC This is what you monitor in production (also feeds the pipeline UI's data-quality tab).

# COMMAND ----------

display(spark.sql(f"""
    SELECT timestamp, origin.flow_name,
           details:flow_progress.data_quality.expectations AS expectations,
           details:flow_progress.metrics.num_output_rows   AS output_rows
    FROM event_log(TABLE({CATALOG}.sdp_demo.silver_orders_checked))
    WHERE event_type = 'flow_progress'
      AND details:flow_progress.data_quality.expectations IS NOT NULL
    ORDER BY timestamp DESC
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cleanup (after the demo)

# COMMAND ----------

# spark.sql(f"DROP SCHEMA IF EXISTS {CATALOG}.sdp_demo CASCADE")
# spark.sql(f"DROP VOLUME IF EXISTS {CATALOG}.{BRONZE_SCHEMA}.landing_sdp")
# print("Demo artifacts removed. Also delete the pipeline in the UI.")
