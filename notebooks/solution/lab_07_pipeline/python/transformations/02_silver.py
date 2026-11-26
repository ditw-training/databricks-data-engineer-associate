# RetailHub sales star: Silver layer (Lab 07)
# Clean orders, the quarantine for bad orders, and the current state of each customer.
from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.table(name="silver_orders", comment="Orders that pass the data-quality rules; returns (negative amounts) stay")
@dp.expect_or_drop("valid_order_id", "order_id IS NOT NULL")
@dp.expect_or_drop("valid_customer", "customer_id IS NOT NULL")
@dp.expect_or_drop("valid_order_time", "order_ts IS NOT NULL")
@dp.expect("non_negative_amount", "total_amount >= 0")
def silver_orders():
    return (
        spark.readStream.table("bronze_orders")
        .select(
            "order_id",
            "customer_id",
            "product_id",
            "store_id",
            F.col("order_datetime").cast("timestamp").alias("order_ts"),
            F.col("order_datetime").cast("date").alias("order_date"),
            "quantity",
            "unit_price",
            "discount_percent",
            "total_amount",
            (F.col("total_amount") < 0).alias("is_return"),
            "payment_method",
            "_source_file",
        )
    )


@dp.table(name="silver_orders_quarantine", comment="Orders that break a drop rule of silver_orders, kept for inspection and replay")
def silver_orders_quarantine():
    return (
        spark.readStream.table("bronze_orders")
        .where("NOT (order_id IS NOT NULL AND customer_id IS NOT NULL AND order_datetime IS NOT NULL)")
    )


dp.create_streaming_table(
    name="silver_customers",
    comment="Current state of each customer for operations: a change overwrites the row",
)

dp.create_auto_cdc_flow(
    target="silver_customers",
    source="bronze_customers",
    keys=["customer_id"],
    sequence_by="_ingested_at",
    except_column_list=["_rescued_data", "_source_file", "_ingested_at"],
    stored_as_scd_type=1,
)
