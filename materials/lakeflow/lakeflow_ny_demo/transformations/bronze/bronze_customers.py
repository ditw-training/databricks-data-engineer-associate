from pyspark import pipelines as dp
from pyspark.sql.functions import col, lit, current_timestamp


@dp.table(
    name="bronze_customers",
    comment="Raw customer data ingested from JSON files using Auto Loader - simulates real-time customer updates for SCD demo. Includes record_type column to distinguish original vs modified records."
)
def bronze_customers():
    """
    Bronze layer: Ingest customer data from Volumes using Auto Loader
    Reads JSON files from /Volumes/<YOUR_CATALOG>/default/datasets/dataset/lakeflow_demo/tpch_customer/
    ⚠️ Replace 'retailhub_trainer' in the .load() path with your own catalog name!
    """
    
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load("/Volumes/retailhub_trainer/default/datasets/dataset/lakeflow_demo/tpch_customer/")
        .withColumn("ingestion_timestamp", current_timestamp())
    )
