# Databricks notebook source
# MAGIC %md
# MAGIC # env_demo — which environment am I running in?
# MAGIC
# MAGIC Deployed by the `env_demo` bundle (`materials/cicd_environments/`). The job passes
# MAGIC `env_name`, `catalog`, `schema` and `min_rows` as job parameters; their values come
# MAGIC from the **bundle target** (`-t dev|test|prod`). The task records one row per run in
# MAGIC `<catalog>.<schema>.env_demo_runs`, so each environment writes to its own schema.

# COMMAND ----------

dbutils.widgets.text("env_name", "local")
dbutils.widgets.text("catalog", "")
dbutils.widgets.text("schema", "")
dbutils.widgets.text("min_rows", "1")

env_name = dbutils.widgets.get("env_name")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
min_rows = int(dbutils.widgets.get("min_rows"))

if not catalog or not schema:
    raise ValueError("catalog and schema must be passed as job parameters (deploy with the bundle)")

print(f"Environment : {env_name}")
print(f"Target table: {catalog}.{schema}.env_demo_runs")
print(f"min_rows    : {min_rows}")

# COMMAND ----------

from pyspark.sql import functions as F

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

# A tiny "quality gate" whose strictness depends on the environment
source_rows = spark.table("samples.nyctaxi.trips").limit(5000).count()
status = "PASSED" if source_rows >= min_rows else "FAILED"
print(f"Quality gate: {source_rows} source rows vs min_rows={min_rows} -> {status}")

(spark.createDataFrame(
    [(env_name, catalog, schema, min_rows, source_rows, status)],
    "env_name string, catalog string, schema string, min_rows int, source_rows long, gate string")
 .withColumn("run_ts", F.current_timestamp())
 .write.mode("append").saveAsTable(f"{catalog}.{schema}.env_demo_runs"))

display(spark.table(f"{catalog}.{schema}.env_demo_runs").orderBy(F.desc("run_ts")))

if status == "FAILED":
    raise Exception(f"[{env_name}] quality gate failed: {source_rows} < {min_rows}")
