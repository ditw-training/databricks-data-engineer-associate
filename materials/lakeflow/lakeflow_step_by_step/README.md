# DEMO 1 — Lakeflow Spark Declarative Pipelines, step by step (build from scratch)

Trainer-driven, ~35–45 min. You build a bronze → silver → gold pipeline **incrementally**, showing:
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

1. **Jobs & Pipelines → Create → ETL pipeline**, serverless, **development mode ON**.
2. Root folder = this folder; source = `transformations/`.
3. Default catalog = your `retailhub_<slug>`, default schema = `sdp_demo` (create it or let the pipeline create it).
4. **Configuration** (Advanced): key `source_path` = `/Volumes/<catalog>/bronze/landing_sdp` (the driver notebook prints the exact value).

## Walkthrough (the demo script)

| Step | What you do | What you say / show |
|---|---|---|
| 1 | Run driver notebook **Step 1** (creates landing dirs, copies **wave 1** of orders + `customers.csv`) | "Files land in a Volume — the pipeline will discover them." |
| 2 | Start with ONLY `01_bronze_orders.py` in the pipeline (or comment the rest out). **Run pipeline** | Bronze ST materializes; graph shows one node. Row count = wave 1. |
| 3 | **Run pipeline again without new files** | **0 rows processed** — this is the checkpoint story: every streaming table/flow keeps its own checkpoint in pipeline-managed storage; already-seen files are never reprocessed. Full refresh = reset checkpoint + rebuild. |
| 4 | Driver **Step 2** (copies wave 2), run pipeline | Only the NEW files' rows are ingested. Show `DESCRIBE HISTORY` + the update's "streaming update" metrics. |
| 5 | Add `02_silver_customers_scd.py`, run | Two silver tables from one CDC feed: **SCD1** (overwrite in place) vs **SCD2** (`__START_AT`/`__END_AT` history columns). |
| 6 | Driver **Step 3** (copies `customers_new.csv` — 15 changed customers), run pipeline, then driver **Step 4** (compare SCD1 vs SCD2 for `CUST000001`) | SCD1: city simply changed. SCD2: old row closed (`__END_AT` set), new current row opened. |
| 7 | Add `03_gold_daily_sales.sql`, run | MV recomputes from silver — contrast **ST (incremental, append-driven)** vs **MV (recomputed result, may refresh incrementally when possible)**. |
| 8 | Add `04_expectations.py`, run | `expect_or_drop` silently filters ~3% dirty rows — show the **data quality** tab / event log metrics. Then UNCOMMENT the `expect_or_fail` block, run → pipeline **fails** (show the error surface), re-comment, run again. |
| 9 | Add `05_quarantine.py`, run | Production pattern: don't lose dropped rows — route them to a quarantine table with the inverse predicate; show counts add up (valid + quarantined = bronze). |
| 10 | Driver **Step 5** — event log queries | `event_log(TABLE(...))` → expectations metrics per update; this is what you monitor in production. |

## Teaching notes

- Keep **development mode ON** → cluster reuse, no retries — fast iteration during the demo.
- The FAIL step really fails the update — that is the point; time-box it (~3 min).
- If short on time, cut step 9 (quarantine) — it is repeated in LAB 07's Task 7.
- Everything here lands in schema `sdp_demo`, so it never collides with the LAB 07 pipeline (`lakeflow_demo`).
