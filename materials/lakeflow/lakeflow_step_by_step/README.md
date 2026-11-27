# DEMO 1 — Lakeflow Spark Declarative Pipelines, step by step (build from scratch)

Trainer-driven. You build a bronze → silver → gold pipeline **incrementally**, showing:
incremental file ingestion + checkpoints → AUTO CDC (SCD1 vs SCD2) → gold MV → expectations (DROP → FAIL → quarantine).

> DEMO 2 (the "current stack") is the finished pipeline in `../lakeflow_demo` — full star schema with flows/backfill.
> DEMO 3 (metadata-driven) is in `../lakeflow_metadata_driven`.

## Files

| File | Stage | Language |
|---|---|---|
| `00_demo_driver.py` | Notebook (NOT part of the pipeline) — prepares landing folders, drops file "waves", inspects results & event log between pipeline updates | notebook |
| `transformations/01_bronze_orders.py` | Bronze ST from `read_files`/Auto Loader — incremental ingestion & checkpoints | Python (`dp`) |
| `transformations/02_silver_customers_scd.py` | AUTO CDC — SCD1 and SCD2 side by side | Python (`dp`) |
| `transformations/03_gold_daily_sales.sql` | Gold materialized view with aggregations | SQL |
| `transformations/04_expectations.py` | Expectations: DROP ROW, then (commented) FAIL | Python (`dp`) |
| `transformations/05_quarantine.py` | Quarantine pattern — valid/invalid split | Python (`dp`) |

## Pipeline setup (once)

1. **Jobs & Pipelines → Create → ETL pipeline**, serverless.
2. Root folder = this folder; source code path = only `transformations/01_bronze_orders.py` (**Configure paths** accepts single files). The other files show as excluded in the editor tree. To add one later in the walkthrough: right-click it in the tree → **Include as pipeline source code**, then **Run pipeline**.
3. Default catalog = your `retailhub_<slug>`, default schema = `sdp_demo` (create it or let the pipeline create it).
4. **Configuration** (Advanced): key `source_path` = `/Volumes/<catalog>/bronze/landing_sdp` (the driver notebook prints the exact value).

## Walkthrough (the demo script)

| Step | What you do | What you say / show |
|---|---|---|
| 1 | Run driver notebook **Step 1** (creates landing dirs, copies **wave 1** of orders + `customers.csv`) | "Files land in a Volume — the pipeline will discover them." |
| 2 | The pipeline has ONLY `01_bronze_orders.py` (setup step 2). **Run pipeline** | Bronze ST materializes; graph shows one node. Row count = wave 1. |
| 3 | **Run pipeline again without new files** | **0 rows processed** — this is the checkpoint story: every streaming table/flow keeps its own checkpoint in pipeline-managed storage; already-seen files are never reprocessed. Full refresh = reset checkpoint + rebuild. |
| 4 | Driver **Step 2** (copies wave 2), run pipeline | Only the NEW files' rows are ingested. Show `DESCRIBE HISTORY` + the update's "streaming update" metrics. |
| 5 | Include `02_silver_customers_scd.py` (right-click → **Include as pipeline source code**), run | Two silver tables from one CDC feed: **SCD1** (overwrite in place) vs **SCD2** (`__START_AT`/`__END_AT` history columns). |
| 6 | Driver **Step 3** (copies `customers_new.csv` — 14 rows: 7 existing customers with changed attributes, 6 new customers, 1 unchanged), run pipeline, then driver **Step 4** (compare SCD1 vs SCD2 for `CUST000001`) | SCD1: city simply changed. SCD2: old row closed (`__END_AT` set), new current row opened. |
| 7 | Include `03_gold_daily_sales.sql`, run | MV recomputes from silver — contrast **ST (incremental, append-driven)** vs **MV (recomputed result, may refresh incrementally when possible)**. |
| 8 | Include `04_expectations.py`, run | `expect_all_or_drop` silently filters the dirty rows — 4 rules × ~3% each ≈ **12%** of bronze (verified: 3,603 of 30,000) — show the **data quality** tab / event log metrics. Then UNCOMMENT the `expect_or_fail` line and run with **Full refresh** of `silver_orders_checked` (pipeline editor: select the table → *Run* ▸ *Full refresh selection*) → the update **FAILS** on the 1,827 returns (negative `total_amount`). A plain run does **not** fail: the streaming table only checks NEW rows and there are none. Show the error surface, re-comment, full-refresh the table again. |
| 9 | Include `05_quarantine.py`, run | Production pattern: don't lose dropped rows — route them to a quarantine table with the inverse predicate; show counts add up (valid + quarantined = bronze). |
| 10 | Driver **Step 5** — event log queries | `event_log(TABLE(...))` → expectations metrics per update; this is what you monitor in production. |

## Teaching notes

- Nothing to switch on: the pipeline editor has no development mode toggle, and runs started from the editor do not retry (automatic recovery is the default only for scheduled and job runs), so iteration is fast.
- The FAIL step really fails the update — only with a **full refresh** of `silver_orders_checked` (a normal run has no new rows to check); keep it short.
- If short on time, cut step 9 (quarantine) — it is repeated in LAB 07's Task 7.
- Everything here lands in schema `sdp_demo`, so it never collides with the LAB 07 pipeline (`lakeflow_demo`).
