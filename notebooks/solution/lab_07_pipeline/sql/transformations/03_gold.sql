-- RetailHub sales star: Gold layer (Lab 07)
-- The star schema: two dimensions and the fact table that joins them.

CREATE OR REFRESH STREAMING TABLE dim_customer
COMMENT 'Customer dimension for marketing: a change closes the old row and adds a new one';

CREATE FLOW dim_customer_cdc AS AUTO CDC INTO dim_customer
FROM STREAM(bronze_customers)
KEYS (customer_id)
SEQUENCE BY _ingested_at
COLUMNS * EXCEPT (_rescued_data, _source_file, _ingested_at)
STORED AS SCD TYPE 2;

-- Task 6: dim_product keeps only the current attributes of each product.
-- To switch it on, select the lines below and press Ctrl+/ (Cmd+/ on a Mac).
CREATE OR REFRESH STREAMING TABLE dim_product
COMMENT 'Product dimension: current attributes only';

CREATE FLOW dim_product_cdc AS AUTO CDC INTO dim_product
FROM STREAM(bronze_products)
KEYS (product_id)
SEQUENCE BY _ingested_at
COLUMNS * EXCEPT (_rescued_data, _source_file, _ingested_at)
STORED AS SCD TYPE 1;

CREATE OR REFRESH MATERIALIZED VIEW fact_sales
COMMENT 'One row per valid order, with the current customer and the product'
AS SELECT
  o.order_id,
  o.order_ts,
  o.order_date,
  o.customer_id,
  c.customer_segment,
  c.city,
  o.product_id,
  p.product_name,
  p.brand,
  o.store_id,
  o.quantity,
  o.unit_price,
  o.total_amount,
  o.is_return,
  o.payment_method
FROM silver_orders o
LEFT JOIN dim_customer c
  ON o.customer_id = c.customer_id AND c.__END_AT IS NULL
LEFT JOIN dim_product p
  ON o.product_id = p.product_id;

CREATE OR REFRESH MATERIALIZED VIEW daily_sales
COMMENT 'Revenue per day and customer segment'
AS SELECT
  order_date,
  coalesce(customer_segment, 'Unknown') AS customer_segment,
  count(*) AS order_lines,
  count_if(is_return) AS returns,
  sum(total_amount) AS revenue
FROM fact_sales
GROUP BY ALL;
