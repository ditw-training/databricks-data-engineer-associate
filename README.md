# Databricks Data Engineer Associate — Training (3 Days)

## About This Repository

Training materials for the **Databricks Certified Data Engineer Associate** certification preparation course — practical, engineering-first, built around one continuous business scenario (**RetailHub**: raw retail data → Bronze → Silver → Gold → Lakeflow pipeline → job orchestration → bundle deployment → monitoring → governance).

**3 days** | ~50% hands-on

Exam: **45 scored questions, 90 minutes, $200.** Passing score is **not published** (set statistically by Databricks) — aim for ≥80% on practice quizzes. PySpark-dominant, with SQL for ingestion, DDL and governance.
Exam guide version: **May 4, 2026** (re-check the official guide ~2 weeks before your exam date — it is revised every 4–6 months).

---

## Exam Domains (May 4, 2026 — current)

| # | Domain | Weight |
|---|--------|--------|
| 1 | Databricks Intelligence Platform | 6% |
| 2 | Data Ingestion and Loading | 21% |
| 3 | Data Transformation and Modeling | 22% |
| 4 | Working with Lakeflow Jobs | 16% |
| 5 | Implementing CI/CD | 10% |
| 6 | Troubleshooting, Monitoring, and Optimization | 10% |
| 7 | Governance and Security | 15% |

> 🔥 The current exam puts strong emphasis on **Lakeflow Connect**, **Lakeflow Spark Declarative Pipelines**, **Lakeflow Jobs**, **Declarative Automation Bundles (formerly Databricks Asset Bundles)**, Spark-UI troubleshooting and **Unity Catalog ABAC**.

---

## Training Structure

| Day | Demos | Labs | Focus |
|-----|-------|------|-------|
| **Day 1** | 00, 01, 02, 02a, 03 | lab_01, lab_02, lab_03 | Platform & UC, ingestion, **Lakeflow Connect (live demo)**, Delta Lake |
| **Day 2** | 04, 05, 06, 07 | lab_04, lab_05, lab_07 | Optimization, incremental ingestion (Auto Loader), medallion, Lakeflow Spark Declarative Pipelines |
| **Day 3** | 08, 09 (+09a), 10, 11 | lab_08, lab_09, lab_troubleshooting, lab_10 | Lakeflow Jobs, CI/CD & bundles, troubleshooting, governance, exam prep |
| **Self-study** | 05a | lab_06 | Transformations & modeling (exam domain 3, 22%) — 10-minute briefing on Day 2, work through after class |

The full timed agenda lives in `notebooks/day1/demo/00_intro.ipynb` and `docs/INSTRUCTOR_GUIDE.md`.

---

## Demo Notebooks

| # | Notebook | Path |
|---|----------|------|
| 00 | Training Introduction & Agenda | `notebooks/day1/demo/00_intro.ipynb` |
| 01 | Platform & Workspace | `notebooks/day1/demo/01_platform_and_workspace.ipynb` |
| 02 | Data Reading & File Formats | `notebooks/day1/demo/02_data_ingestion.ipynb` |
| 02a | **Lakeflow Connect — managed SQL Server connector (live demo)** | `notebooks/day1/demo/02a_lakeflow_connect_demo.ipynb` |
| 03 | Delta Lake Fundamentals | `notebooks/day1/demo/03_delta_lake.ipynb` |
| B03 | Bonus: Delta Advanced (CDF, CLONE) | `notebooks/day1/demo/BONUS_03_delta_advanced.ipynb` |
| 05a | **Transformations & Modeling (self-study)** — joins, windows, dedup, tuning configs | `notebooks/day2/demo/05a_transformations.ipynb` |
| 04 | Delta Optimization — Liquid Clustering, predictive optimization, deletion vectors | `notebooks/day2/demo/04_delta_optimization.ipynb` |
| 05 | Incremental Ingestion — COPY INTO, Auto Loader | `notebooks/day2/demo/05_incremental_ingestion.ipynb` |
| 06 | Medallion Architecture — Bronze → Silver → Gold | `notebooks/day2/demo/06_medallion_architecture.ipynb` |
| B05 | Bonus: Streaming Advanced | `notebooks/day2/demo/BONUS_05_streaming_advanced.ipynb` |
| 07 | Lakeflow Spark Declarative Pipelines | `notebooks/day2/demo/07_lakeflow_pipelines.ipynb` |
| 08 | Lakeflow Jobs — Orchestration | `notebooks/day3/demo/08_job_orchestration.ipynb` |
| 09 | CI/CD & Declarative Automation Bundles | `notebooks/day3/demo/09_cicd_and_automation.ipynb` |
| 09a | DABs per environment — one bundle, dev / test / prod targets (trainer demo) | `notebooks/day3/demo/09a_dabs_environments.ipynb` + `materials/cicd_environments/` |
| 10 | Governance & Security (incl. ABAC) | `notebooks/day3/demo/10_governance_and_security.ipynb` |
| 11 | Exam Preparation | `notebooks/day3/demo/11_exam_preparation.ipynb` |
| BT | Bonus: Troubleshooting Reference (Spark UI, failures) | `notebooks/day3/demo/BONUS_troubleshooting.ipynb` |

---

## Labs

Every lab follows the same pattern: *Scenario → tasks with `# TODO` → Guidance hints → validation asserts → review*. Guides (hints) are in `notebooks/guides/`, full answers in `notebooks/solution/`.

| Lab | Topic | Day | Guide | Solution |
|-----|-------|-----|:---:|:---:|
| lab_01 | Platform & Workspace First Steps (Serverless, UC, Volumes) | 1 | ✅ | ✅ |
| lab_02 | Batch Ingestion (readers, schemas, CTAS) | 1 | ✅ | ✅ |
| lab_03 | Delta DML & Time Travel | 1 | ✅ | ✅ |
| lab_06 | Transformations & Modeling (joins, windows, dedup) | self-study | ✅ | ✅ |
| lab_04 | Delta Optimization (OPTIMIZE, Liquid Clustering, CLUSTER BY AUTO) | 2 | ✅ | ✅ |
| lab_05 | Incremental Ingestion & Auto Loader | 2 | ✅ | ✅ |
| lab_07 | Lakeflow Spark Declarative Pipeline (build & run) | 2 | ✅ | ✅ |
| lab_08 | Lakeflow Jobs Orchestration (for_each, triggers, repair) | 3 | ✅ | ✅ |
| lab_09 | CI/CD — deploy the RetailHub bundle (DABs) | 3 | ✅ | ✅ |
| lab_troubleshooting | Debug a broken job/pipeline (Spark UI, run history) | 3 | — | ✅ |
| lab_10 | Governance & Security (GRANT/REVOKE, masks, row filters) | 3 | ✅ | ✅ |

Lab locations: `notebooks/day1/lab/`, `notebooks/day2/lab/`, `notebooks/day3/lab/`.

---

## Bonus Notebooks

| Notebook | Topic | Path |
|----------|-------|------|
| BONUS_aibi_dashboards | AI/BI Dashboards & Genie | `notebooks/bonus/BONUS_aibi_dashboards.ipynb` |
| BONUS_timestamps_autoloader_archive | Timestamps, UTC & Auto Loader Archiving | `notebooks/bonus/BONUS_timestamps_autoloader_archive.ipynb` |
| BONUS_powerbi_direct_query | Power BI Live Direct Query Demo | `notebooks/bonus/BONUS_powerbi_direct_query.ipynb` |
| BONUS_external_connection | ADLS External Location — manual runbook (automated by `infra/terraform`) | `notebooks/bonus/BONUS_external_connection.ipynb` |

---

## Setup

1. **Infrastructure (optional but recommended):** `infra/terraform/` provisions everything reproducibly — ADLS Gen2 + access connector + UC external location, optional premium workspace (14-day trial), and the **Azure SQL Database (AdventureWorksLT, CDC)** used by the Lakeflow Connect demo. See `infra/terraform/README.md`. Enable CDC afterwards with `infra/sql/enable_cdc.sql`.
   ⚠️ Coordinate `terraform apply/destroy` timing — do not run during another training on the same subscription.
2. **Workspace pre-config (trainer, once):** `notebooks/setup/00_pre_config.ipynb` — creates per-user catalogs `retailhub_<slug>`, schemas, volumes, copies datasets, sets grants. Includes a **smoke test** section — run it the day before.
3. **Per-notebook setup (automatic):** `notebooks/setup/00_setup.ipynb` is invoked via `%run` from every notebook and exports `CATALOG`, `BRONZE_SCHEMA`, `SILVER_SCHEMA`, `GOLD_SCHEMA`, `DATASET_PATH`.

---

## Participant Documents (PDF)

Built for both languages into `docs/ENG/` and `docs/PL/` (same file names):

| PDF | Content |
|---|---|
| `cheatsheet_databricks_data_engineer.pdf` | Reference guide — one chapter per module (01–10, 02a, 05a, troubleshooting workshop) + exam at a glance |
| `quiz_databricks_data_engineer.pdf` | 68 questions for Days 1–3 with answer key |
| `exam_objectives_map.pdf` | All 32 objectives of the May 2026 exam guide mapped to modules and labs |
| `next_steps.pdf` | Exam preparation, study plan, learning path, features beyond the exam |
| `external_connection_guide.pdf` | Connecting Unity Catalog to ADLS Gen2 (manual steps + Terraform mapping) |
| `lakeflow_connect_sqlserver_guide.pdf` | Lakeflow Connect managed SQL Server connector on the course's Azure SQL Database |
| `pyspark_vs_sparksql.pdf` | PySpark and Spark SQL side by side for ingestion and transformations |

Sources are Markdown files in `utilization/en/` and `utilization/pl/` (local only, git-ignored); rebuild with `./scripts/build_pdfs.sh [document] [ENG|PL]` (requires `pandoc` and `weasyprint`). Quiz notebooks in `utilization/quiz/` share the same answer key.

---

## Repository Structure

```
.
├── README.md
├── docs/
│   ├── INSTRUCTOR_GUIDE.md            # Agenda grids, checklists, per-lab notes
│   ├── ENG/                           # Participant PDFs (English)
│   └── PL/                            # Participant PDFs (Polish)
├── infra/
│   ├── terraform/                     # ADLS + UC + workspace + Azure SQL (AdventureWorks, CDC)
│   └── sql/enable_cdc.sql             # CDC enablement for the Lakeflow Connect demo
├── assets/images/                     # Notebook images & UI screenshots
├── dataset/
│   ├── customers/                     # customers.csv, customers_new.csv, xlsx
│   ├── orders/                        # orders_batch.json, stream/*.json (waves 1–3)
│   ├── products/                      # products.csv, products.parquet
│   ├── demo/                          # stream waves 4–6 (Auto Loader increments)
│   └── workshop/                      # AdventureWorks CSVs (bonus/homework)
├── materials/
│   ├── lakeflow/                      # 3 pipeline variants (see materials/lakeflow/README.md)
│   ├── medallion/                     # Medallion layer notebooks (job-chainable)
│   ├── orchestration/                 # Job task scripts (triggers, task values)
│   ├── cicd/                          # Declarative Automation Bundle (databricks.yml + resources)
│   └── troubleshooting/broken_job/    # Deliberately broken tasks for lab_troubleshooting
├── scripts/build_pdfs.sh              # Markdown → PDF build (pandoc + WeasyPrint)
└── notebooks/
    ├── setup/                         # 00_pre_config (trainer) + 00_setup (%run)
    ├── day1/{demo,lab}/               # 00–03 + 02a | lab_01–lab_03
    ├── day2/{demo,lab}/               # 04, 05, 05a, 06, 07 | lab_04–lab_07
    ├── day3/{demo,lab}/               # 08–11 | lab_08, lab_09_dabs, lab_10, lab_troubleshooting
    ├── guides/                        # Hint notebooks (no full answers)
    ├── solution/                      # Full solutions (run top-to-bottom)
    └── bonus/                         # Optional extras
```

---

## Sources & Conventions

- Exam alignment: official **May 4, 2026** exam guide (Databricks).
- Platform naming as of 2026: **Lakeflow Spark Declarative Pipelines** (formerly DLT), **Lakeflow Jobs** (formerly Workflows), **Declarative Automation Bundles** (formerly Databricks Asset Bundles), **Git folders** (formerly Repos), serverless-first compute.
- Notebooks in English; the Polish slide deck is `PL-Databricks-Data-Engineering.pdf`.
