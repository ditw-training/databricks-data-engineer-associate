-- RetailHub sales star: Gold layer (Lab 07)
-- The star schema: two dimensions and the fact table that joins them.

-- Task 5: paste the code from the Workshop Guide here

-- Task 6: dim_product keeps only the current attributes of each product.
-- To switch it on, select the lines below and press Ctrl+/ (Cmd+/ on a Mac).
-- CREATE OR REFRESH STREAMING TABLE dim_product
-- COMMENT 'Product dimension: current attributes only';

-- CREATE FLOW dim_product_cdc AS AUTO CDC INTO dim_product
-- FROM STREAM(bronze_products)
-- KEYS (product_id)
-- SEQUENCE BY _ingested_at
-- COLUMNS * EXCEPT (_rescued_data, _source_file, _ingested_at)
-- STORED AS SCD TYPE 1;

-- Task 7: paste the code from the Workshop Guide here

-- Task 9: paste the code from the Workshop Guide here
