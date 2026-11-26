-- RetailHub sales star: Silver layer (Lab 07)
-- Clean orders, the quarantine for bad orders, and the current state of each customer.

CREATE OR REFRESH STREAMING TABLE silver_orders (
  CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_customer EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_order_time EXPECT (order_ts IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT non_negative_amount EXPECT (total_amount >= 0)
)
COMMENT 'Orders that pass the data-quality rules; returns (negative amounts) stay'
AS SELECT
  order_id,
  customer_id,
  product_id,
  store_id,
  CAST(order_datetime AS TIMESTAMP) AS order_ts,
  CAST(order_datetime AS DATE) AS order_date,
  quantity,
  unit_price,
  discount_percent,
  total_amount,
  total_amount < 0 AS is_return,
  payment_method,
  _source_file
FROM STREAM(bronze_orders);

CREATE OR REFRESH STREAMING TABLE silver_orders_quarantine
COMMENT 'Orders that break a drop rule of silver_orders, kept for inspection and replay'
AS SELECT *
FROM STREAM(bronze_orders)
WHERE NOT (order_id IS NOT NULL AND customer_id IS NOT NULL AND order_datetime IS NOT NULL);

CREATE OR REFRESH STREAMING TABLE silver_customers
COMMENT 'Current state of each customer for operations: a change overwrites the row';

CREATE FLOW silver_customers_cdc AS AUTO CDC INTO silver_customers
FROM STREAM(bronze_customers)
KEYS (customer_id)
SEQUENCE BY _ingested_at
COLUMNS * EXCEPT (_rescued_data, _source_file, _ingested_at)
STORED AS SCD TYPE 1;
