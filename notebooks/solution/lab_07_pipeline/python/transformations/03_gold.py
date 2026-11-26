# RetailHub sales star: Gold layer (Lab 07)
# The star schema: two dimensions and the fact table that joins them.
from pyspark import pipelines as dp
from pyspark.sql import functions as F


dp.create_streaming_table(
    name="dim_customer",
    comment="Customer dimension for marketing: a change closes the old row and adds a new one",
)

dp.create_auto_cdc_flow(
    target="dim_customer",
    source="bronze_customers",
    keys=["customer_id"],
    sequence_by="_ingested_at",
    except_column_list=["_rescued_data", "_source_file", "_ingested_at"],
    stored_as_scd_type=2,
)

# Task 6: dim_product keeps only the current attributes of each product.
# To switch it on, select the lines below and press Ctrl+/ (Cmd+/ on a Mac).
dp.create_streaming_table(name="dim_product", comment="Product dimension: current attributes only")

dp.create_auto_cdc_flow(
    target="dim_product",
    source="bronze_products",
    keys=["product_id"],
    sequence_by="_ingested_at",
    except_column_list=["_rescued_data", "_source_file", "_ingested_at"],
    stored_as_scd_type=1,
)


@dp.materialized_view(name="fact_sales", comment="One row per valid order, with the current customer and the product")
def fact_sales():
    orders = spark.read.table("silver_orders")
    customers = (
        spark.read.table("dim_customer")
        .where("__END_AT IS NULL")
        .select("customer_id", "customer_segment", "city")
    )
    products = spark.read.table("dim_product").select("product_id", "product_name", "brand")
    return (
        orders.join(customers, "customer_id", "left")
        .join(products, "product_id", "left")
        .select(
            "order_id",
            "order_ts",
            "order_date",
            "customer_id",
            "customer_segment",
            "city",
            "product_id",
            "product_name",
            "brand",
            "store_id",
            "quantity",
            "unit_price",
            "total_amount",
            "is_return",
            "payment_method",
        )
    )


@dp.materialized_view(name="daily_sales", comment="Revenue per day and customer segment")
def daily_sales():
    return (
        spark.read.table("fact_sales")
        .groupBy("order_date", F.coalesce("customer_segment", F.lit("Unknown")).alias("customer_segment"))
        .agg(
            F.count("*").alias("order_lines"),
            F.count_if("is_return").alias("returns"),
            F.sum("total_amount").alias("revenue"),
        )
    )
