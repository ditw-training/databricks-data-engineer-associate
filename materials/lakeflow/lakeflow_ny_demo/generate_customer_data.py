"""
Data Generator for Customer SCD Demo

Usage:
1. Run generate_batch_0() once to create initial historical data
2. Run generate_batch_1() through generate_batch_5() sequentially to simulate changes
3. Each batch creates a new JSON file in /Volumes/<YOUR_CATALOG>/default/datasets/dataset/lakeflow_demo/tpch_customer/

The pipeline's Auto Loader will automatically detect and process new files.
"""

from pyspark.sql.functions import col, when, concat, lit, current_timestamp, to_json, struct
from pyspark.sql.types import LongType, DoubleType, DateType
import json

# ⚠️ IMPORTANT: Replace 'retailhub_trainer' with YOUR OWN catalog name!
# Each participant gets their own catalog created by the trainer (e.g. retailhub_jan, retailhub_anna).
# Ask your trainer for your catalog name if you're not sure.
TARGET_PATH = "/Volumes/retailhub_trainer/default/datasets/dataset/lakeflow_demo/tpch_customer/"
ORDERS_PATH  = "/Volumes/retailhub_trainer/default/datasets/dataset/lakeflow_demo/tpch_orders/"


def generate_batch_0():
    """
    Generate Batch 0: Historical/Original Customer Data
    
    This creates the initial dataset from samples.tpch.customer.
    All records are marked as 'original' type.
    """
    print("Generating Batch 0: Historical customer data...")
    
    df = (
        spark.read.table("samples.tpch.customer")
        .withColumn("record_type", lit("original"))
        .withColumn("processing_timestamp", current_timestamp())
    )
    
    output_path = f"{TARGET_PATH}batch_0_original.json"
    df.write.mode("overwrite").json(output_path)
    
    count = df.count()
    print(f"✓ Batch 0 complete: {count} records written to {output_path}")
    return df


def generate_batch_1():
    """
    Generate Batch 1: First Wave of Updates
    
    Simulates address and phone changes for every 1000th customer.
    """
    print("Generating Batch 1: Address and phone updates...")
    
    df = (
        spark.read.table("samples.tpch.customer")
        .filter((col("c_custkey") % 1000) == 0)
        .withColumn("c_address", concat(lit("UPDATED_V1: "), col("c_address")))
        .withColumn("c_phone", concat(lit("99-"), col("c_phone")))
        .withColumn("record_type", lit("modified"))
        .withColumn("processing_timestamp", current_timestamp())
    )
    
    output_path = f"{TARGET_PATH}batch_1_updates.json"
    df.write.mode("overwrite").json(output_path)
    
    count = df.count()
    print(f"✓ Batch 1 complete: {count} records written to {output_path}")
    return df


def generate_batch_2():
    """
    Generate Batch 2: Market Segment and Balance Changes
    
    Simulates market segment switches and account balance increases for every 500th customer.
    """
    print("Generating Batch 2: Market segment and balance updates...")
    
    df = (
        spark.read.table("samples.tpch.customer")
        .filter((col("c_custkey") % 500) == 0)
        .withColumn("c_mktsegment", 
            when(col("c_mktsegment") == "BUILDING", "AUTOMOBILE")
            .when(col("c_mktsegment") == "AUTOMOBILE", "FURNITURE")
            .when(col("c_mktsegment") == "MACHINERY", "HOUSEHOLD")
            .otherwise("BUILDING")
        )
        .withColumn("c_acctbal", col("c_acctbal") + 1500)
        .withColumn("record_type", lit("modified"))
        .withColumn("processing_timestamp", current_timestamp())
    )
    
    output_path = f"{TARGET_PATH}batch_2_updates.json"
    df.write.mode("overwrite").json(output_path)
    
    count = df.count()
    print(f"✓ Batch 2 complete: {count} records written to {output_path}")
    return df


def generate_batch_3():
    """
    Generate Batch 3: Comprehensive Updates
    
    Simulates comprehensive changes (address, phone, segment, balance, comment) for every 750th customer.
    """
    print("Generating Batch 3: Comprehensive updates...")
    
    df = (
        spark.read.table("samples.tpch.customer")
        .filter((col("c_custkey") % 750) == 0)
        .withColumn("c_address", concat(lit("UPDATED_V2: "), col("c_address")))
        .withColumn("c_phone", concat(lit("88-"), col("c_phone")))
        .withColumn("c_mktsegment", lit("MACHINERY"))
        .withColumn("c_acctbal", col("c_acctbal") - 800)
        .withColumn("c_comment", concat(lit("[MODIFIED_V3] "), col("c_comment")))
        .withColumn("record_type", lit("modified"))
        .withColumn("processing_timestamp", current_timestamp())
    )
    
    output_path = f"{TARGET_PATH}batch_3_updates.json"
    df.write.mode("overwrite").json(output_path)
    
    count = df.count()
    print(f"✓ Batch 3 complete: {count} records written to {output_path}")
    return df


def generate_batch_4():
    """
    Generate Batch 4: Different Customer Set
    
    Simulates updates for every 333rd customer (different set than previous batches).
    """
    print("Generating Batch 4: New customer set updates...")
    
    df = (
        spark.read.table("samples.tpch.customer")
        .filter((col("c_custkey") % 333) == 0)
        .withColumn("c_address", concat(lit("NEW_ADDR_V4: "), col("c_address")))
        .withColumn("c_phone", concat(lit("77-"), col("c_phone")))
        .withColumn("c_acctbal", col("c_acctbal") + 2500)
        .withColumn("record_type", lit("modified"))
        .withColumn("processing_timestamp", current_timestamp())
    )
    
    output_path = f"{TARGET_PATH}batch_4_updates.json"
    df.write.mode("overwrite").json(output_path)
    
    count = df.count()
    print(f"✓ Batch 4 complete: {count} records written to {output_path}")
    return df


def generate_batch_5():
    """
    Generate Batch 5: Re-updates (Overlapping with Batch 1)
    
    Simulates re-updating the same customers from Batch 1 (every 1000th customer).
    This demonstrates how SCD handles multiple updates to the same records.
    """
    print("Generating Batch 5: Re-updates (overlapping with Batch 1)...")
    
    df = (
        spark.read.table("samples.tpch.customer")
        .filter((col("c_custkey") % 1000) == 0)
        .withColumn("c_address", concat(lit("FINAL_UPDATE: "), col("c_address")))
        .withColumn("c_phone", concat(lit("66-"), col("c_phone")))
        .withColumn("c_mktsegment", lit("HOUSEHOLD"))
        .withColumn("c_acctbal", col("c_acctbal") + 5000)
        .withColumn("c_comment", concat(lit("[FINAL_VERSION] "), col("c_comment")))
        .withColumn("record_type", lit("modified"))
        .withColumn("processing_timestamp", current_timestamp())
    )
    
    output_path = f"{TARGET_PATH}batch_5_updates.json"
    df.write.mode("overwrite").json(output_path)
    
    count = df.count()
    print(f"✓ Batch 5 complete: {count} records written to {output_path}")
    return df


def generate_all_batches():
    """
    Generate all batches sequentially.
    """
    print("=" * 60)
    print("Generating ALL batches for SCD Demo")
    print("=" * 60)
    
    generate_batch_0()
    generate_batch_1()
    generate_batch_2()
    generate_batch_3()
    generate_batch_4()
    generate_batch_5()
    
    print("=" * 60)
    print("✓ All batches generated successfully!")
    print(f"Files location: {TARGET_PATH}")
    print("=" * 60)


def generate_orders_clean():
    """
    Generate clean orders batch (baseline).

    Writes a sample of real TPC-H orders to the orders volume so that
    bronze_orders (cloudFiles) can pick them up.
    Run this BEFORE the dirty batches to establish baseline data.
    """
    print("Generating clean orders baseline...")

    df = spark.read.table("samples.tpch.orders").limit(200)

    output_path = f"{ORDERS_PATH}batch_clean.json"
    df.write.mode("overwrite").json(output_path)

    count = df.count()
    print(f"✓ Clean orders: {count} records written to {output_path}")
    return df


def generate_dirty_orders_validation():
    """
    Generate orders with records that violate expect_or_drop / expect_all_or_drop rules.

    Expected behaviour in silver_orders_cleaned (pipeline DOES NOT stop):
    - Records with o_custkey IS NULL   → dropped by expect_or_drop
    - Records with o_totalprice < 0    → dropped by expect_all_or_drop
    - Records with o_orderdate IS NULL → dropped by expect_all_or_drop
    - Clean records                    → pass through normally

    After running, refresh the pipeline and check the Expectations tab –
    you will see non-zero DROP counts for the rules above.
    """
    print("Generating dirty orders (validation / drop demo)...")

    df_clean = spark.read.table("samples.tpch.orders").limit(10)

    # Null custkey  →  expect_or_drop fires
    df_null_custkey = (
        spark.read.table("samples.tpch.orders")
        .limit(5)
        .withColumn("o_custkey", lit(None).cast(LongType()))
    )

    # Negative price  →  expect_all_or_drop fires
    df_neg_price = (
        spark.read.table("samples.tpch.orders")
        .limit(5)
        .withColumn("o_totalprice", lit(-999.99).cast(DoubleType()))
    )

    # Null orderdate  →  expect_all_or_drop fires
    df_null_date = (
        spark.read.table("samples.tpch.orders")
        .limit(5)
        .withColumn("o_orderdate", lit(None).cast(DateType()))
    )

    df = df_clean.unionByName(df_null_custkey).unionByName(df_neg_price).unionByName(df_null_date)

    output_path = f"{ORDERS_PATH}batch_dirty_validation.json"
    df.write.mode("overwrite").json(output_path)

    count = df.count()
    print(f"✓ Dirty validation batch: {count} records ({count - 10} bad) written to {output_path}")
    print("  → Pipeline will continue; bad records will be dropped.")
    return df


def generate_dirty_orders_fail():
    """
    Generate orders with a NULL o_orderkey — triggers expect_or_fail.

    Expected behaviour in silver_orders_cleaned:
    - ANY record with o_orderkey IS NULL causes the pipeline to STOP with an error.

    ⚠️  Use this only to demonstrate pipeline failure.
        After the demo, delete this file from the volume and re-run the pipeline
        to restore normal operation.
    """
    print("Generating dirty orders (FAIL demo — pipeline will stop)...")

    df_clean = spark.read.table("samples.tpch.orders").limit(10)

    # Null orderkey  →  expect_or_fail fires and STOPS the pipeline
    df_null_key = (
        spark.read.table("samples.tpch.orders")
        .limit(1)
        .withColumn("o_orderkey", lit(None).cast(LongType()))
    )

    df = df_clean.unionByName(df_null_key)

    output_path = f"{ORDERS_PATH}batch_dirty_fail.json"
    df.write.mode("overwrite").json(output_path)

    count = df.count()
    print(f"✓ Dirty FAIL batch: {count} records (1 null orderkey) written to {output_path}")
    print("  ⚠️  Next pipeline run will FAIL on expect_or_fail rule.")
    print(f"  To recover: delete {output_path} from the volume and restart the pipeline.")
    return df


# Example usage (uncomment to run):
generate_batch_0()  # Start with historical data
# generate_batch_1()  # Then run incremental batches one by one
# generate_batch_2()
# generate_batch_3()
# generate_batch_4()
# generate_batch_5()

# --- Expectations demo ---
# generate_orders_clean()             # 1. Seed clean orders first
# generate_dirty_orders_validation()  # 2. Drop demo  — pipeline continues
# generate_dirty_orders_fail()        # 3. Fail demo  — pipeline stops ⚠️
