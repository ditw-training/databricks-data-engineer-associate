# Databricks notebook source
# MAGIC %md
# MAGIC # RetailHub Broken Job — Task 3: Publish Daily Sales
# MAGIC Aggregates enriched orders into `gold.ts_daily_sales` for the BI team.
# MAGIC
# MAGIC > ⚠️ **This notebook is DELIBERATELY BROKEN** — it is the subject of
# MAGIC > `lab_troubleshooting`. Compare the table it reads with the table the
# MAGIC > upstream task actually produces, and check its `depends_on` in the
# MAGIC > job definition.

# COMMAND ----------

# Parameters from the Job
dbutils.widgets.text("catalog", "retailhub_trainer")

CATALOG = dbutils.widgets.get("catalog")
print(f"Catalog: {CATALOG}")

# COMMAND ----------

from pyspark.sql import functions as F

# NOTE: the silver table was renamed during the refactor ("_final" felt
# cleaner"), but nobody checked what the transform task actually writes.
# In the job definition this task also depends only on ingest, so even a
# correct name could be read BEFORE the transform task has produced it.
SOURCE = f"{CATALOG}.silver.ts_orders_final"

daily_sales = (
    spark.table(SOURCE)
    .groupBy(F.to_date("order_datetime").alias("order_date"), "country")
    .agg(
        F.count("*").alias("order_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
        F.round(F.avg("total_amount"), 2).alias("avg_order_value"),
    )
)

# COMMAND ----------

TARGET = f"{CATALOG}.gold.ts_daily_sales"
daily_sales.write.mode("overwrite").saveAsTable(TARGET)
print(f"Written: {TARGET} ({spark.table(TARGET).count()} rows)")

# COMMAND ----------

import json
dbutils.notebook.exit(json.dumps({"status": "SUCCESS", "table": TARGET}))
