# RetailHub sales star: Bronze layer (Lab 07)
# Raw files from the landing folders under source_path, read incrementally.
# Each table adds two columns from the file metadata: the file a row came from and the time the file arrived.
from pyspark import pipelines as dp
from pyspark.sql import functions as F

SOURCE_PATH = spark.conf.get("source_path")  # pipeline settings: Configuration -> source_path


# Task 1: paste the code from the Workshop Guide here
