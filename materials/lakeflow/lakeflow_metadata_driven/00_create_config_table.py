# Databricks notebook source
# MAGIC %md
# MAGIC # DEMO 3 — Config table for the metadata-driven pipeline
# MAGIC
# MAGIC 👨‍🏫 **TRAINER notebook** — run BEFORE creating the pipeline. Not part of the pipeline source.
# MAGIC
# MAGIC The pipeline (`transformations/01_dynamic_pipeline.py`) reads this table at update start
# MAGIC and generates one bronze (+ optional silver) dataset **per row**.

# COMMAND ----------

# MAGIC %run ../../../notebooks/setup/00_setup

# COMMAND ----------

CONFIG_SCHEMA = f"{CATALOG}.sdp_meta"
CONFIG_TABLE = f"{CONFIG_SCHEMA}.pipeline_config"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CONFIG_SCHEMA}")

spark.sql(f"""
CREATE OR REPLACE TABLE {CONFIG_TABLE} (
  entity        STRING  NOT NULL COMMENT 'Logical source name; drives dataset names',
  source_subdir STRING  NOT NULL COMMENT 'Folder under ${{source_path}}',
  source_format STRING  NOT NULL COMMENT 'csv | json | parquet',
  load_type     STRING  NOT NULL COMMENT 'append | scd1 | scd2',
  primary_keys  ARRAY<STRING>    COMMENT 'CDC keys (scd1/scd2 only)',
  sequence_col  STRING           COMMENT 'CDC ordering column (scd1/scd2 only)',
  expectations  MAP<STRING, STRING> COMMENT 'rule name -> SQL predicate (ON VIOLATION DROP)',
  active        BOOLEAN NOT NULL COMMENT 'false = skip this entity'
) COMMENT 'Metadata-driven pipeline definition: 1 row = 1 ingestion flow'
""")

# COMMAND ----------

spark.sql(f"""
INSERT INTO {CONFIG_TABLE} VALUES
  ('customers', 'customers', 'csv', 'scd1',
   array('customer_id'), '_ingest_ts',
   map('valid_customer_id', 'customer_id IS NOT NULL'),
   true),

  ('orders', 'orders', 'json', 'append',
   NULL, NULL,
   map('valid_order_id',    'order_id IS NOT NULL',
       'valid_customer_id', 'customer_id IS NOT NULL',
       'valid_datetime',    'order_datetime IS NOT NULL'),
   true),

  ('products', 'products', 'csv', 'scd2',
   array('product_id'), '_ingest_ts',
   map('valid_product_id', 'product_id IS NOT NULL'),
   true)
""")

display(spark.table(CONFIG_TABLE))

print("Pipeline Configuration keys to set:")
print(f"  source_path  = {DATASET_PATH}")
print(f"  config_table = {CONFIG_TABLE}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎬 Live wow-moment (Step 4 of the walkthrough)
# MAGIC Run this AFTER the first successful pipeline update, then start a new update:
# MAGIC a brand-new table appears in the graph — **no code changed**.

# COMMAND ----------

# spark.sql(f"""
# INSERT INTO {CONFIG_TABLE} VALUES
#   ('orders_stream', 'orders/stream', 'json', 'append',
#    NULL, NULL,
#    map('valid_order_id', 'order_id IS NOT NULL'),
#    true)
# """)
# display(spark.table(CONFIG_TABLE))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5 — deactivate an entity (and re-run the update)

# COMMAND ----------

# spark.sql(f"UPDATE {CONFIG_TABLE} SET active = false WHERE entity = 'products'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cleanup (after the demo)

# COMMAND ----------

# spark.sql(f"DROP SCHEMA IF EXISTS {CONFIG_SCHEMA} CASCADE")
# print("Demo schema removed. Also delete the pipeline in the UI.")
