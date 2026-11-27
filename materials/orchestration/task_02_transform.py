# Databricks notebook source
# MAGIC %md
# MAGIC # Task 2: Transform Data
# MAGIC Reads the upstream `row_count` task value, applies transformations  
# MAGIC (duration, cost per mile). Publishes `rows_transformed` as a task value.

# COMMAND ----------

from pyspark.sql import functions as F
from datetime import date

# Parameters
dbutils.widgets.text("source_table", "samples.nyctaxi.trips")
dbutils.widgets.text("run_date", "")

source_table = dbutils.widgets.get("source_table")
run_date = dbutils.widgets.get("run_date") or str(date.today())

# COMMAND ----------

# Read the task value published by the upstream "validate" task.
# debugValue -> used when running this notebook interactively (outside a job)
# default    -> used in a job run if the key was not set upstream
rows_validated = dbutils.jobs.taskValues.get(
    taskKey="validate",
    key="row_count",
    default=0,
    debugValue=0
)
print(f"Rows validated upstream: {rows_validated}")

# COMMAND ----------

# Transformation
df = spark.table(source_table)

df_transformed = (
    df
    .withColumn("trip_duration_minutes",
                F.round((F.col("tpep_dropoff_datetime").cast("long") -
                         F.col("tpep_pickup_datetime").cast("long")) / 60, 2))
    .withColumn("cost_per_mile",
                F.when(F.col("trip_distance") > 0,
                       F.round(F.col("fare_amount") / F.col("trip_distance"), 2))
                .otherwise(0))
    .withColumn("processing_date", F.lit(run_date))
)

row_count = df_transformed.count()
print(f"Transformed {row_count} rows")

display(df_transformed.select(
    "trip_distance", "fare_amount", "trip_duration_minutes", "cost_per_mile"
).limit(5))

# COMMAND ----------

# Publish result for downstream tasks
dbutils.jobs.taskValues.set(key="rows_transformed", value=row_count)
