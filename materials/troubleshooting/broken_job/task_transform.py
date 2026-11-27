# Databricks notebook source
# MAGIC %md
# MAGIC # RetailHub Broken Job — Task 2: Enrich Orders
# MAGIC Joins Bronze orders with the customers file into `silver.ts_orders_enriched`.
# MAGIC
# MAGIC > ⚠️ **This notebook is DELIBERATELY BROKEN** — it is the subject of
# MAGIC > `lab_troubleshooting`. It *runs*, but look at the row counts, the task
# MAGIC > count, and the shuffle metrics in the Spark UI / query profile.

# COMMAND ----------

# Parameters from the Job
dbutils.widgets.text("catalog", "retailhub_trainer")

CATALOG = dbutils.widgets.get("catalog")
print(f"Catalog: {CATALOG}")

# COMMAND ----------

# "Performance tuning" a teammate copied from a blog post about a 50 TB cluster.
spark.conf.set("spark.sql.shuffle.partitions", "4000")
print("shuffle partitions:", spark.conf.get("spark.sql.shuffle.partitions"))

# COMMAND ----------

from pyspark.sql import functions as F

orders    = spark.table(f"{CATALOG}.bronze.ts_orders_raw")
customers = (
    spark.read.format("csv")
    .option("header", True)
    .load(f"/Volumes/{CATALOG}/default/datasets/customers/customers.csv")
)

# Join orders to customers.
# NOTE: "customer ids sometimes have suffix noise, matching on the first
# 8 characters is more robust" — famous last words of the same teammate.
enriched = orders.join(
    customers,
    F.substring(orders["customer_id"], 1, 8) == F.substring(customers["customer_id"], 1, 8),
    "inner",
).select(
    orders["*"],
    customers["first_name"],
    customers["last_name"],
    customers["city"],
    customers["country"],
    customers["customer_segment"],
)

# COMMAND ----------

TARGET = f"{CATALOG}.silver.ts_orders_enriched"
enriched.write.mode("overwrite").saveAsTable(TARGET)

in_rows  = orders.count()
out_rows = spark.table(TARGET).count()
print(f"orders in : {in_rows:>12,}")
print(f"rows out  : {out_rows:>12,}")   # <- an enrichment join should NOT multiply rows

# COMMAND ----------

import json
dbutils.notebook.exit(json.dumps({"status": "SUCCESS", "table": TARGET, "row_count": out_rows}))
