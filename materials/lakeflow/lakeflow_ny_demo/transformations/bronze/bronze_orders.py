from pyspark import pipelines as dp

# ⚠️ IMPORTANT: Replace 'retailhub_trainer' with YOUR OWN catalog name!
ORDERS_PATH = "/Volumes/retailhub_trainer/default/datasets/dataset/lakeflow_demo/tpch_orders/"

@dp.table(
    name="bronze_orders",
    comment="Raw orders data ingested from JSON files via Auto Loader — enables expectations demo with dirty data injection"
)
def bronze_orders():
    """
    Bronze layer: Ingest orders data from Volumes using Auto Loader.

    Reads from the orders volume instead of samples.tpch.orders directly,
    so that generate_dirty_orders_validation() and generate_dirty_orders_fail()
    can inject controlled bad records to demonstrate all expectation types
    in silver_orders_cleaned.

    Use generate_customer_data.py → generate_orders_clean() to seed the initial data.
    """
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(ORDERS_PATH)
    )
