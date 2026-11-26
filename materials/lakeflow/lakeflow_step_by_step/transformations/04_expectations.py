# =====================================================================
# STAGE 4 — EXPECTATIONS: warn -> DROP ROW -> FAIL UPDATE
# =====================================================================
# DEMO SCRIPT:
#   Run A: as-is -> @dp.expect_all_or_drop removes the dirty rows: 4 rules x ~3%
#          each = ~12% of bronze (NULL ids/timestamps/payment). Show the
#          pipeline's data-quality metrics and compare counts vs bronze.
#   Run B: UNCOMMENT the expect_or_fail line below and run with a FULL REFRESH
#          of silver_orders_checked -> the update FAILS on the amount rule
#          (1,827 returns have total_amount < 0). A plain run does NOT fail:
#          a streaming table only checks NEW rows, and there are none. Show the error in the UI,
#          explain when to fail-fast (contract violations, financial data),
#          then RE-COMMENT and full-refresh silver_orders_checked once more.
#   Modes recap:
#     @dp.expect(...)              -> keep row, only METRIC (warn)
#     @dp.expect_all_or_drop({...})-> drop bad rows silently (metrics kept)
#     @dp.expect_or_fail(...)      -> abort the update on first violation
# =====================================================================

from pyspark import pipelines as dp

RULES = {
    "valid_order_id":    "order_id IS NOT NULL",
    "valid_customer_id": "customer_id IS NOT NULL",
    "valid_datetime":    "order_datetime IS NOT NULL",
    "valid_payment":     "payment_method IS NOT NULL",
}


@dp.table(
    name="silver_orders_checked",
    comment="Orders gated by expectations: dirty rows are DROPPED (metrics in event log).",
    table_properties={"quality": "silver"},
)
@dp.expect_all_or_drop(RULES)
# --- Run B: uncomment the line below, run the pipeline, watch it FAIL ---
# @dp.expect_or_fail("amount_positive", "total_amount > 0")
def silver_orders_checked():
    return spark.readStream.table("bronze_orders_sdp")

# SQL equivalent (for the screen):
#
#   CREATE OR REFRESH STREAMING TABLE silver_orders_checked (
#     CONSTRAINT valid_order_id    EXPECT (order_id IS NOT NULL)    ON VIOLATION DROP ROW,
#     CONSTRAINT valid_customer_id EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW,
#     CONSTRAINT amount_positive   EXPECT (total_amount > 0)        ON VIOLATION FAIL UPDATE
#   )
#   AS SELECT * FROM STREAM bronze_orders_sdp;
