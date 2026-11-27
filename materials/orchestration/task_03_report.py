# Databricks notebook source
# MAGIC %md
# MAGIC # Task 3: Generate Report
# MAGIC Aggregates metrics (total trips, revenue, avg fare/distance).  
# MAGIC Displays the summary report.

# COMMAND ----------

from pyspark.sql import functions as F

# Parameters
dbutils.widgets.text("source_table", "samples.nyctaxi.trips")

source_table = dbutils.widgets.get("source_table")

# COMMAND ----------

# Aggregations
df = spark.table(source_table)

report = df.agg(
    F.count("*").alias("total_trips"),
    F.round(F.sum("fare_amount"), 2).alias("total_revenue"),
    F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
    F.round(F.avg("trip_distance"), 2).alias("avg_distance"),
    F.round(F.max("fare_amount"), 2).alias("max_fare")
)

# COMMAND ----------

# Daily report (total trips and revenue go to task values below)
display(report.select("avg_fare", "avg_distance", "max_fare"))

# COMMAND ----------

# Publish headline metrics as task values (visible in the run's task output)
metrics = report.first()
dbutils.jobs.taskValues.set(key="total_trips", value=int(metrics.total_trips))
dbutils.jobs.taskValues.set(key="total_revenue", value=float(metrics.total_revenue))
