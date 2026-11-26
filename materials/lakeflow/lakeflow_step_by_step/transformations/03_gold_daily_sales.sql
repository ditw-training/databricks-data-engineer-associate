-- =====================================================================
-- STAGE 3 — GOLD: materialized view with aggregations
-- =====================================================================
-- DEMO SCRIPT:
--   - Gold layer = business-ready objects. Here: a MATERIALIZED VIEW.
--   - MV vs STREAMING TABLE (exam favorite):
--       * ST  = incremental, append-driven, for ingestion/streaming sources
--       * MV  = a precomputed RESULT of a query; the pipeline keeps it
--               up to date on refresh (incrementally when it can, full
--               recompute when it must — e.g. after non-incremental changes)
--   - MVs can read other pipeline datasets by name; joining the SCD1
--     dimension shows the classic fact-x-dim gold pattern.
-- =====================================================================

CREATE OR REFRESH MATERIALIZED VIEW gold_daily_sales
COMMENT 'Daily revenue and volume by customer segment (business-ready).'
AS
SELECT
  DATE(o.order_datetime)                          AS order_date,
  c.customer_segment,
  COUNT(DISTINCT o.order_id)                      AS orders_cnt,
  SUM(o.total_amount)                             AS revenue,
  AVG(o.total_amount)                             AS avg_order_value,
  APPROX_COUNT_DISTINCT(o.customer_id)            AS active_customers
FROM bronze_orders_sdp o
LEFT JOIN silver_customers_scd1 c USING (customer_id)
GROUP BY DATE(o.order_datetime), c.customer_segment;

-- TALKING POINT: the NULL customer_segment bucket you will see comes from
-- the ~3% dirty orders (missing customer_id) — a perfect segue to STAGE 4
-- (expectations): quality problems surface in GOLD unless you gate SILVER.
