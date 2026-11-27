# DEMO 3 — Metadata-driven Lakeflow Spark Declarative Pipelines

Trainer-driven. One generic pipeline source file + one **config table** generate the whole
bronze/silver graph dynamically — no per-table code.

## Why metadata-driven? (the point of this demo)

| Hand-coded (DEMO 1/2) | Metadata-driven (this demo) |
|---|---|
| 1 dataset = 1 block of code | 1 dataset = **1 row in a config table** |
| Onboarding source #47 = new PR with copy-pasted code | Onboarding = `INSERT INTO pipeline_config ...` |
| Quality rules drift per table | Rules stored centrally in config, applied uniformly |
| Fine for ~5–20 tables | The pattern real projects use for **50–500 ingestion tables** |

Trade-offs to say out loud: the config is read when the update **starts** (change a row → next update picks it up);
logic errors surface at graph-evaluation time; don't over-engineer — with 5 tables, plain code is clearer.

## Files

| File | Role |
|---|---|
| `00_create_config_table.py` | Notebook (NOT pipeline source): creates `<catalog>.sdp_meta.pipeline_config` + seed rows, then the "add a row live" cell |
| `transformations/01_dynamic_pipeline.py` | The ONLY pipeline source file — loops over config rows and emits datasets |

## Config table shape

One row per entity. `load_type` decides the silver pattern:

| entity | source_subdir | format | load_type | keys | sequence_col | expectations (JSON) |
|---|---|---|---|---|---|---|
| customers | customers | csv | **scd1** | customer_id | `_ingest_ts` | `{"valid_id":"customer_id IS NOT NULL"}` |
| orders | orders | json | **append** | — | — | `{"valid_order":"order_id IS NOT NULL", ...}` |
| products | products | csv | **scd2** | product_id | `_ingest_ts` | `{"valid_id":"product_id IS NOT NULL"}` |

> `customers/*.csv` matches both `customers.csv` and `customers_new.csv`, and `_ingest_ts` is the file modification time. SCD1 therefore keeps the values of the file written last. On the test workspace `customers_new.csv` landed 1 s after `customers.csv`, so the changed values win. If the files land in another order, SCD1 shows the old values without any error.

## Pipeline setup

1. Run `00_create_config_table.py` first (creates schema `sdp_meta` + the table).
2. Create an ETL pipeline: source = `transformations/`, default catalog = your `retailhub_<slug>`, default schema = `sdp_meta`, serverless, dev mode.
3. Configuration keys:
   - `source_path`   = value printed by the notebook (the datasets Volume)
   - `config_table`  = `<catalog>.sdp_meta.pipeline_config`

## Walkthrough

| Step | Do | Say |
|---|---|---|
| 1 | Show the config table (3 rows) | "The pipeline's shape lives in DATA, not code." |
| 2 | Open `01_dynamic_pipeline.py` | One loop; factory functions. Closure pitfall: the factories already pin each row, so it does not happen here. It appears only if you put `@dp.table` directly in the `for` loop: every table then reads the LAST row. |
| 3 | Run the pipeline | Graph shows 3 bronze + 2 SCD silver + 1 checked silver — all from 3 config rows. |
| 4 | **Live wow-moment:** run the "add a row" cell in the notebook (`orders_stream` entity), start a new update | A NEW table appears in the graph — zero code changed. `orders/stream/` in the repo has 3 files (30,000 rows). If the Volume also has `orders_stream_004.json`, the table has 40,000 rows. |
| 5 | Flip `active = false` for one entity, update again | Dataset disappears from the graph (table remains in UC until dropped). |

## Where this shows up in the real world / exam

- Real world: ingestion frameworks (one per company…), Lakeflow Connect internally is metadata-driven too.
- Exam angle: this is **beyond the exam outline** — but it cements ST vs MV, AUTO CDC and expectations,
  which ARE exam topics. Say that explicitly.
