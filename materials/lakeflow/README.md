# Lakeflow Pipeline Variants — which one is used when

This folder holds **five** Lakeflow Spark Declarative Pipeline codebases. They overlap on purpose (same medallion pattern, different datasets/APIs/teaching goals). Use them as follows:

| Variant | Language / API | Dataset | Used in |
|---|---|---|---|
| `lakeflow_step_by_step/` | **Python + SQL, progressive** (Auto Loader + checkpoints → AUTO CDC SCD1/SCD2 → gold MV → expectations DROP/FAIL/quarantine) | RetailHub (`dataset/`) | **DEMO 1 in module 07** — trainer builds the pipeline from scratch, stage by stage; driver notebook drops file waves between updates |
| `lakeflow_demo/` | **SQL** (`CREATE OR REFRESH STREAMING TABLE`, `CREATE FLOW … INSERT INTO ONCE`, expectations, gold star schema) | RetailHub (`dataset/`) | **DEMO 2 (the finished stack)**, **LAB 07** and the Day-3 capstone thread; also deployed by the `materials/cicd/` bundle in **LAB 09** |
| `lakeflow_metadata_driven/` | **Python, dynamic** (config table `pipeline_config` → one generic file emits the whole graph; factory functions, closure pitfalls) | RetailHub (`dataset/`) | **DEMO 3 in module 07** — metadata-driven ingestion framework pattern (*beyond exam*, flagged; homework / fast finishers) |
| `lakeflow_ny_demo/` | **Python** (`from pyspark import pipelines as dp`, `dp.create_auto_cdc_flow` — SCD1 vs SCD2 side by side) | `samples.tpch` → JSON landing files | Spare instructor demo of the Python API — superseded by `lakeflow_step_by_step`. **Not ready to run as-is:** first run `generate_customer_data.py` (`generate_batch_0()` + `generate_orders_clean()`), which writes landing files to hard-coded `/Volumes/retailhub_trainer/default/datasets/dataset/lakeflow_demo/…` paths (edit the catalog); without them the pipeline fails with `CF_EMPTY_DIR_FOR_SCHEMA_INFERENCE`. Verified: ~750k customers → slow on small compute |
| `lakeflow_bonus/` | SQL + Python (`@dp.append_flow`, Auto Loader `cloudFiles`, `${source_path}` config) | AdventureWorks (`dataset/workshop/Lakeflow/`) | **Optional homework** / bonus workshop only |

Rule of thumb for the training: participants touch **only `lakeflow_demo`** (LAB 07/09); everything else is trainer material. Each demo folder carries its own `README.md` walkthrough script.
