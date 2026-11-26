# RetailHub sales star: Gold layer (Lab 07)
# The star schema: two dimensions and the fact table that joins them.
from pyspark import pipelines as dp
from pyspark.sql import functions as F


# Task 5: paste the code from the Workshop Guide here

# Task 6: dim_product keeps only the current attributes of each product.
# To switch it on, select the lines below and press Ctrl+/ (Cmd+/ on a Mac).
# dp.create_streaming_table(name="dim_product", comment="Product dimension: current attributes only")

# dp.create_auto_cdc_flow(
#     target="dim_product",
#     source="bronze_products",
#     keys=["product_id"],
#     sequence_by="_ingested_at",
#     except_column_list=["_rescued_data", "_source_file", "_ingested_at"],
#     stored_as_scd_type=1,
# )


# Task 7: paste the code from the Workshop Guide here


# Task 9: paste the code from the Workshop Guide here
