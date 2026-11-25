# Databricks Data Engineer Associate — Training (3 Days)

## About This Repository

Training materials for the **Databricks Certified Data Engineer Associate** certification preparation course — practical, engineering-first, built around one continuous business scenario (**RetailHub**: raw retail data → Bronze → Silver → Gold → Lakeflow pipeline → job orchestration → bundle deployment → monitoring → governance).

**3 days** | ~50% hands-on

Exam: **45 scored questions, 90 minutes, $200.** Passing score is **not published** (set statistically by Databricks) — aim for ≥80% on practice quizzes. SQL and Python (PySpark) — SQL where possible.
Exam guide version: exam published **May 4, 2026**, guide updated **August 6, 2026** (re-check the official guide ~2 weeks before your exam date — it is revised every 4–6 months).

---

## Exam Domains (exam published May 4, 2026, guide updated August 6, 2026)

| # | Domain | Weight |
|---|--------|--------|
| 1 | Databricks Intelligence Platform | 6% |
| 2 | Data Ingestion and Loading | 21% |
| 3 | Data Transformation and Modeling | 22% |
| 4 | Working with Lakeflow Jobs | 16% |
| 5 | Implementing CI/CD | 10% |
| 6 | Troubleshooting, Monitoring, and Optimization | 10% |
| 7 | Governance and Security | 15% |

> The current exam puts strong emphasis on **Lakeflow Connect**, **Lakeflow Spark Declarative Pipelines**, **Lakeflow Jobs**, **Declarative Automation Bundles (formerly Databricks Asset Bundles)**, Spark-UI troubleshooting and **Unity Catalog ABAC**.

---

## Training Structure

| Day | Demos | Labs | Focus |
|-----|-------|------|-------|
| **Day 1** | 01, 02, 03, 04 (+BONUS_04) | Lab 01 quiz (app), lab_02 (app), lab_03, lab_04 | Platform & UC, batch ingestion, Delta Lake, incremental ingestion (COPY INTO, Auto Loader) |
| **Day 2** | 04a, 05a/05b, 06, 07 | lab_06, lab_07 | **Lakeflow Connect (live demo)**, transformations (theory in the deck; 05a PySpark and 05b SQL for self-training), Delta optimization, medallion (theory in the deck), Lakeflow Spark Declarative Pipelines (07: theory, then lab_07 in which participants build the pipeline) |
| **Day 3** | 08, 09, 10, BONUS_troubleshooting §2–3 | lab_08, lab_09, lab_10 (app), lab_troubleshooting | Lakeflow Jobs, CI/CD & bundles, governance, troubleshooting, exam prep |

The full timed agenda lives in `docs/INSTRUCTOR_GUIDE.md` (§1 Agenda).

---

## Demo Notebooks

| # | Notebook | Path |
|---|----------|------|
| 01 | Platform & Workspace | `notebooks/day1/demo/01_platform_and_workspace.ipynb` |
| 02 | Data Reading & File Formats | `notebooks/day1/demo/02_data_ingestion.ipynb` |
| 03 | Delta Lake Fundamentals — incl. Change Data Feed; CLONE at the end (if time allows) | `notebooks/day1/demo/03_delta_lake.ipynb` |
| 04 | Incremental Ingestion — COPY INTO, Auto Loader | `notebooks/day1/demo/04_incremental_ingestion.ipynb` |
| B04 | Bonus: Streaming Advanced | `notebooks/day1/demo/BONUS_04_streaming_advanced.ipynb` |
| 04a | **Lakeflow Connect — managed SQL Server connector (live demo)** | `notebooks/day2/demo/04a_lakeflow_connect_demo.ipynb` |
| 05a | **Transformations in PySpark (self-training)** — joins, windows, dedup, tuning configs | `notebooks/day2/demo/05a_transformations_pyspark.ipynb` |
| 05b | **Transformations in SQL (self-training)** — the same objectives in SQL | `notebooks/day2/demo/05b_transformations_sql.ipynb` |
| 06 | Delta Optimization — Liquid Clustering, partitioning, predictive optimization, deletion vectors | `notebooks/day2/demo/06_delta_optimization.ipynb` |
| 07 | Lakeflow Spark Declarative Pipelines — theory in class (no live build; the build is lab_07) | `notebooks/day2/demo/07_lakeflow_pipelines.ipynb` |
| 08 | Lakeflow Jobs — Orchestration | `notebooks/day3/demo/08_job_orchestration.ipynb` |
| 09 | CI/CD & Declarative Automation Bundles: Git folders, bundles, one bundle deployed to dev / test (trainer demo) | `notebooks/day3/demo/09_cicd_and_bundles.ipynb` + `materials/cicd_environments/` |
| 10 | Governance & Security (incl. ABAC) | `notebooks/day3/demo/10_governance_and_security.ipynb` |
| BT | Bonus: Troubleshooting Reference (Spark UI, failures) | `notebooks/day3/demo/BONUS_troubleshooting.ipynb` |

---

## Labs

Every lab follows the same pattern: *Scenario → tasks with `# TODO` → Guidance hints → validation asserts → review*. Full answers are in `notebooks/solution/`.

| Lab | Topic | Day | Solution |
|-----|-------|-----|:---:|
| lab_02 | Batch Ingestion (readers, schemas, CTAS) — in the Workshop Guide app only, no notebook | 1 | — |
| lab_03 | Delta DML & Time Travel | 1 | ✅ |
| lab_04 | Incremental Ingestion & Auto Loader | 1 | ✅ |
| lab_06 | Delta Optimization (OPTIMIZE, Liquid Clustering, CLUSTER BY AUTO) | 2 | ✅ |
| lab_07 | Lakeflow Spark Declarative Pipeline — build it step by step in the Lakeflow Pipelines Editor, SQL or Python: bronze + silver with expectations and quarantine, SCD1 + SCD2, `dim_product` + `fact_sales` (Tasks 8–9 stretch) | 2 | ✅ |
| lab_08 | Lakeflow Jobs Orchestration (for_each, triggers, repair) | 3 | ✅ |
| lab_09 | CI/CD — deploy the RetailHub bundle (DABs) | 3 | ✅ |
| lab_troubleshooting | Debug a broken job/pipeline (Spark UI, run history) | 3 | ✅ |
| lab_10 | Governance & Security (GRANT/REVOKE, masks, row filters) — in the Workshop Guide app only, no notebook | 3 | — |

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
| `cheatsheet_databricks_data_engineer.pdf` | Reference guide — one chapter per module (01–10, 03a, 05a, troubleshooting workshop) + exam at a glance |
| `quiz_databricks_data_engineer.pdf` | 70 questions for Days 1–3 with answer key |
| `exam_objectives_map.pdf` | All 33 objectives of the exam guide (updated 6 Aug 2026) mapped to modules and labs |
| `next_steps.pdf` | Exam preparation, study plan, learning path, features beyond the exam |
| `external_connection_guide.pdf` | Connecting Unity Catalog to ADLS Gen2 (manual steps + Terraform mapping) |
| `lakeflow_connect_sqlserver_guide.pdf` | Lakeflow Connect managed SQL Server connector on the course's Azure SQL Database |
| `pyspark_vs_sparksql.pdf` | PySpark and Spark SQL side by side for ingestion and transformations |

Sources are Markdown files in `utilization/en/` and `utilization/pl/` (local only, git-ignored); rebuild with `./scripts/build_pdfs.sh [document] [ENG|PL]` (requires `pandoc` and `weasyprint`).

---

## Practice exams

Three take-home practice exams, 50 questions each (150 in total), one best answer per question, 90 minutes per set. The page is a single offline file, `docs/practice_exams.html`: it opens from disk without a network, holds the answers and explanations (EN and PL) and shows the score per exam domain after you submit. Each question points to the demo notebook to revisit. It is practice material, not the official exam; Databricks does not publish the pass mark.

Sources are `utilization/practice_exams/set{1,2,3}.json`. Check and rebuild after any change:

```bash
python3 -I utilization/practice_exams/check_practice_exams.py   # counts, domain weights, 33 objectives, demo links
python3 -I scripts/build_practice_exams.py                      # writes docs/practice_exams.html
```

---

## Workshop Guide app

`apps/workshop-guide/` is a Databricks App (`dbxacad-dea-guide`, AppKit, TypeScript/React) for the classroom. It serves seven lab guides: five notebook labs (lab03, lab04, lab06, lab07, lab08) with **Check your work** on the participant's own tables, and two app-only labs (lab02, lab10) whose tasks are exercises in the app. It also serves the quizzes, PL/EN, graded on the server: the three day quizzes from `utilization/{en,pl}/quiz.md` (20, 20 and 30 questions), the lab quizzes `quiz_lab01` and `quiz_lab09` from `utilization/{en,pl}/quiz_labs.md`, and a locked mock exam (practice set 1) as plan B. Every item stays locked until the trainer opens it in the **Access** panel of `/trainer`; the trainer view shows the group's progress and first-attempt results.

- Deploy with the bundle in the app folder: `databricks bundle deploy --var sql_warehouse_id=<id>` (one SQL warehouse; secrets first).
- `notebooks/setup/00_pre_config` Step 6 creates the progress table `retailhub_dea_trainer.default.workshop_progress` and the quiz key volume, and grants them to the app's service principal only.
- `npm run quiz-from-md` writes the public questions (`apps/workshop-guide/config/quiz/questions.json`) and the answer key `utilization/quiz_key.json` (git-ignored); the trainer uploads the key to the volume.

Steps, unlock flow and details: [`apps/workshop-guide/README.md`](apps/workshop-guide/README.md); contract: [`apps/SPEC_workshop_guide.md`](apps/SPEC_workshop_guide.md).

---

## Repository Structure

```
.
├── README.md
├── docs/
│   ├── INSTRUCTOR_GUIDE.md            # Agenda grids, checklists, per-lab notes
│   ├── practice_exams.html            # Take-home practice exams (offline, built by scripts/build_practice_exams.py)
│   ├── ENG/                           # Participant PDFs (English)
│   └── PL/                            # Participant PDFs (Polish)
├── apps/
│   ├── workshop-guide/                # Workshop Guide app: day quizzes, trainer unlock (bundle in the folder)
│   └── SPEC_workshop_guide.md         # Contract of the app
├── infra/
│   ├── terraform/                     # ADLS + UC + workspace + Azure SQL (AdventureWorks, CDC)
│   └── sql/enable_cdc.sql             # CDC enablement for the Lakeflow Connect demo
├── assets/images/                     # Notebook images & UI screenshots
├── dataset/
│   ├── customers/                     # customers.csv, customers_new.csv, xlsx
│   ├── orders/                        # orders_batch.json, stream/*.json (waves 1–3)
│   ├── products/                      # products.csv, products.parquet
│   └── demo/                          # stream waves 4–6 (Auto Loader increments)
├── materials/
│   ├── lakeflow/                      # 4 pipeline variants (see materials/lakeflow/README.md)
│   ├── medallion/                     # Medallion layer notebooks (job-chainable)
│   ├── orchestration/                 # Job task scripts (task values)
│   ├── cicd/                          # Declarative Automation Bundle (databricks.yml + resources)
│   └── troubleshooting/broken_job/    # Deliberately broken tasks for lab_troubleshooting
├── scripts/build_pdfs.sh              # Markdown → PDF build (pandoc + WeasyPrint) — local only, git-ignored
└── notebooks/
    ├── setup/                         # 00_pre_config (trainer), 00_setup (%run), catalog_slug, 99_test_runner
    ├── day1/{demo,lab}/               # 01–04, BONUS_04 | lab_03, lab_04
    ├── day2/{demo,lab}/               # 04a, 05a, 05b, 06, 07 | lab_06–lab_07
    ├── day3/{demo,lab}/               # 08–10, BONUS_troubleshooting | lab_08, lab_09_dabs, lab_troubleshooting
    ├── solution/                      # Full solutions (run top-to-bottom)
    └── bonus/                         # Optional extras
```

---

## Sources & Conventions

- Exam alignment: official exam guide (Databricks), exam published **May 4, 2026**, guide updated **August 6, 2026**.
- Platform naming as of 2026: **Lakeflow Spark Declarative Pipelines** (formerly DLT), **Lakeflow Jobs** (formerly Workflows), **Declarative Automation Bundles** (formerly Databricks Asset Bundles), **Git folders** (formerly Repos), serverless-first compute.
- Notebooks in English; the Polish slide deck is `docs/PL/PL-Databricks-Data-Engineering.pdf`.
