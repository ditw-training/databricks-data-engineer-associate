------------------------------------------------------------------
-- GOLD – DIM PRODUCT (MV)
------------------------------------------------------------------

CREATE OR REFRESH MATERIALIZED VIEW dim_product
AS
SELECT
  -- UNKNOWN gets -1, the key fact_sales uses for a product it cannot find
  CASE WHEN is_unknown = 1 THEN -1
       ELSE row_number() OVER (ORDER BY is_unknown, product_id) END AS product_key,
  product_id,
  product_name,
  subcategory_code,
  brand,
  unit_cost,
  list_price,
  weight_kg,
  status,
  is_active,
  is_unknown
FROM silver_products;
