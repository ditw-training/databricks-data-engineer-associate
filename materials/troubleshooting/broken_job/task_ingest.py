# Databricks notebook source
# MAGIC %md
# MAGIC # RetailHub Broken Job — Task 1: Ingest Orders
# MAGIC Loads the raw orders JSON from the training Volume into `bronze.ts_orders_raw`.
# MAGIC
# MAGIC > ⚠️ **This notebook is DELIBERATELY BROKEN** — it is the subject of
# MAGIC > `lab_troubleshooting`. Do not "fix" it here; diagnose it from the job
# MAGIC > run history and fix a scratch copy in the lab notebook.

# COMMAND ----------

# Parameters from the Job
dbutils.widgets.text("catalog", "retailhub_trainer")

CATALOG = dbutils.widgets.get("catalog")
print(f"Catalog: {CATALOG}")

# COMMAND ----------

# Read raw orders with an explicit schema (Bronze best practice... in theory)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# NOTE: a teammate "refactored" this cell last Friday.
RAW_ORDERS_PATH = f"/Volumes/{CATALOG}/default/dataset/orders/orders_batch.json"

orders_schema = StructType([
    StructField("order_id",       StringType()),
    StructField("client_id",      StringType()),
    StructField("product_id",     StringType()),
    StructField("store_id",       StringType()),
    StructField("order_datetime", StringType()),
    StructField("quantity",       IntegerType()),
    StructField("unit_price",     DoubleType()),
    StructField("amount_total",   DoubleType()),
    StructField("payment_method", StringType()),
])

orders_df = (
    spark.read
    .format("json")
    .schema(orders_schema)
    .load(RAW_ORDERS_PATH)
)

print(f"Rows read: {orders_df.count()}")

# COMMAND ----------

# Write Bronze table
TARGET = f"{CATALOG}.bronze.ts_orders_raw"
orders_df.write.mode("overwrite").saveAsTable(TARGET)
print(f"Written: {TARGET}")

# COMMAND ----------

# Data quality gate — the customer key and the amount must be populated,
# otherwise every downstream join and aggregation silently produces garbage.
total     = spark.table(TARGET).count()
null_keys = spark.table(TARGET).filter("client_id IS NULL OR amount_total IS NULL").count()

if total == 0 or null_keys == total:
    raise Exception(
        f"INGEST QUALITY GATE FAILED: {null_keys}/{total} rows have NULL "
        f"client_id/amount_total in {TARGET}. Check the reader schema against "
        f"the source file fields."
    )

print(f"Quality gate passed: {total - null_keys}/{total} rows populated")

# COMMAND ----------

import json
dbutils.notebook.exit(json.dumps({"status": "SUCCESS", "table": TARGET, "row_count": total}))
