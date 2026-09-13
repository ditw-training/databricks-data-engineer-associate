# Databricks notebook source
# MAGIC %md
# MAGIC # Task 1: Validate Source Data
# MAGIC Validates row count against `min_rows` threshold.  
# MAGIC Publishes `row_count` / `source_table` to downstream tasks via `dbutils.jobs.taskValues.set()`.

# COMMAND ----------

# Parameters from Job
dbutils.widgets.text("source_table", "samples.nyctaxi.trips")
dbutils.widgets.text("min_rows", "100")

source_table = dbutils.widgets.get("source_table")
min_rows = int(dbutils.widgets.get("min_rows"))

# COMMAND ----------

# Validation
df = spark.table(source_table)
row_count = df.count()

print(f"Source: {source_table}")
print(f"Row count: {row_count}")
print(f"Minimum required: {min_rows}")

if row_count < min_rows:
    raise Exception(f"Validation FAILED: {row_count} rows < {min_rows} minimum")

print("Validation PASSED")

# COMMAND ----------

# Share results with downstream tasks as TASK VALUES.
# NOTE: dbutils.notebook.exit() does NOT create task values — its string only goes to
# a dbutils.notebook.run() caller / the run output. Outside a job, set() does nothing.
dbutils.jobs.taskValues.set(key="row_count", value=row_count)
dbutils.jobs.taskValues.set(key="source_table", value=source_table)
