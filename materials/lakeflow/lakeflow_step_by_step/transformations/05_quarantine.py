# =====================================================================
# STAGE 5 — QUARANTINE: don't lose the bad rows, route them
# =====================================================================
# DEMO SCRIPT:
#   DROP ROW discards data — fine for a demo, risky in production
#   (no reprocessing, no root-cause analysis). The production pattern:
#   split the stream with the SAME rule set:
#     - valid rows      -> silver_orders_valid
#     - violating rows  -> quarantine_orders (+ reason & timestamp)
#   Verify on screen: valid + quarantined == bronze  (nothing lost).
#   Quarantine can then be alerted on, inspected, fixed and replayed.
# =====================================================================

from pyspark import pipelines as dp
from pyspark.sql import functions as F
import functools

RULES = {
    "valid_order_id":    "order_id IS NOT NULL",
    "valid_customer_id": "customer_id IS NOT NULL",
    "valid_datetime":    "order_datetime IS NOT NULL",
    "valid_payment":     "payment_method IS NOT NULL",
}

ALL_VALID = " AND ".join(f"({c})" for c in RULES.values())


@dp.table(
    name="silver_orders_valid",
    comment="Rows passing ALL quality rules.",
    table_properties={"quality": "silver"},
)
def silver_orders_valid():
    return spark.readStream.table("bronze_orders_sdp").where(F.expr(ALL_VALID))


@dp.table(
    name="quarantine_orders",
    comment="Rows violating at least one rule, kept for inspection & replay.",
    table_properties={"quality": "quarantine"},
)
def quarantine_orders():
    df = spark.readStream.table("bronze_orders_sdp").where(~F.expr(ALL_VALID))
    # Record WHICH rules failed — priceless during incident analysis:
    reason_cols = [
        F.when(~F.expr(cond), F.lit(name)) for name, cond in RULES.items()
    ]
    return df.withColumn(
        "_violated_rules", F.array_compact(F.array(*reason_cols))
    ).withColumn("_quarantined_at", F.current_timestamp())

# TALKING POINT: same RULES dict drives both tables — one source of truth.
# In DEMO 3 (metadata-driven) the rules move from code into a CONFIG TABLE.
