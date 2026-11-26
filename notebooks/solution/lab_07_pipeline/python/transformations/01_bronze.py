# RetailHub sales star: Bronze layer (Lab 07)
# Raw files from the landing folders under source_path, read incrementally.
# Each table adds two columns from the file metadata: the file a row came from and the time the file arrived.
from pyspark import pipelines as dp
from pyspark.sql import functions as F

SOURCE_PATH = spark.conf.get("source_path")  # pipeline settings: Configuration -> source_path


def read_landing(folder, file_format):
    """New files of one landing folder (Auto Loader), with the file path and the file time."""
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", file_format)
        .option("cloudFiles.inferColumnTypes", "true")
        .option("header", "true")
        .load(f"{SOURCE_PATH}/{folder}")
        .select(
            "*",
            F.col("_metadata.file_path").alias("_source_file"),
            F.col("_metadata.file_modification_time").alias("_ingested_at"),
        )
    )


@dp.table(name="bronze_orders", comment="Raw orders from the landing folder orders/")
def bronze_orders():
    return read_landing("orders", "json")


@dp.table(name="bronze_customers", comment="Raw customer files: the first snapshot, then the change files")
def bronze_customers():
    return read_landing("customers", "csv")


@dp.table(name="bronze_products", comment="Raw product files")
def bronze_products():
    return read_landing("products", "csv")
