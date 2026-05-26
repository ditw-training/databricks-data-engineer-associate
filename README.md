# Databricks Data Engineer Associate — Training (3 Days)

## About This Repository

Training materials for the **Databricks Data Engineer Associate** certification preparation course.
**3 days × ~5.5h net (990 min)** | 40% demo / 40% workshop / 20% theory

Exam: **45 questions, 90 minutes, ~70% passing score**
Certification guide version: **May 2026**

---

## Exam Domains (Nov 2025)

| Domain | Weight |
|--------|--------|
| Databricks Data Intelligence Platform | 10% |
| Development & Ingestion | 30% |
| Data Processing & Transformations | 31% |
| Productionizing Data Pipelines | 18% |
| Data Governance & Quality | 11% |

---

## Training Structure

| Day | Demo Notebooks | Labs | Focus |
|-----|---------------|------|-------|
| **Day 1** | 00–03 | lab_01 | Intro, Platform, File Formats & Reads, Delta Lake |
| **Day 2** | 04–06 | lab_02, lab_03–lab_05 | Optimization, Incremental Ingestion, Streaming, Medallion Architecture |
| **Day 3** | 07–11 | lab_07–lab_10 | Medallion, Orchestration, CI/CD, Governance, Exam Prep |

---

## Demo Notebooks

| # | Notebook | Path |
|---|----------|------|
| 00 | Training Introduction | `notebooks/day1/demo/00_intro.ipynb` |
| 01 | Platform & Workspace | `notebooks/day1/demo/01_platform_and_workspace.ipynb` |
| 02 | Data Reading & File Formats | `notebooks/day1/demo/02_data_ingestion.ipynb` |
| 03 | Delta Lake Fundamentals | `notebooks/day1/demo/03_delta_lake.ipynb` |
| 04 | Delta Optimization | `notebooks/day2/demo/04_delta_optimization.ipynb` |
| 05 | Incremental Ingestion | `notebooks/day2/demo/05_incremental_ingestion.ipynb` |
| 06 | Medallion Architecture — Bronze → Silver → Gold | `notebooks/day2/demo/06_medallion_architecture.ipynb` |
| 07 | Lakeflow Pipelines | `notebooks/day3/demo/07_lakeflow_pipelines.ipynb` |
| 08 | Job Orchestration | `notebooks/day3/demo/08_job_orchestration.ipynb` |
| 09 | CI/CD & Automation | `notebooks/day3/demo/09_cicd_and_automation.ipynb` |
| 10 | Governance & Security | `notebooks/day3/demo/10_governance_and_security.ipynb` |
| 11 | Exam Preparation | `notebooks/day3/demo/11_exam_preparation.ipynb` |

---

## Labs

| # | Lab | Day | Source | Guide |
|---|-----|-----|--------|-------|
| lab_01 | First Steps & Platform | Day 1 | DEA LAB_01 | lab_01_first_steps_guide |
| lab_02 | Batch & Stream Ingestion (COPY INTO + Auto Loader) | Day 1 | L&T Day1 Workshop | — |
| lab_03 | Delta DML & Time Travel | Day 1 | DEA LAB_03 | lab_03_delta_dml_guide |
| lab_04 | Delta Optimization Workshop | Day 2 | L&T Day2 Workshop | — |
| lab_05 | Streaming & Auto Loader | Day 2 | DEA LAB_05 | lab_05_streaming_guide |
| lab_07 | Lakeflow Declarative Pipeline | Day 3 | DEA LAB_07 | lab_07_lakeflow_pipeline_guide |
| lab_08 | Job Orchestration | Day 3 | DEA LAB_08 | lab_08_orchestration_guide |
| lab_09 | CI/CD & DABs | Day 3 | NEW | — |
| lab_10 | Governance & Security | Day 3 | DEA LAB_09 + DENY task | lab_10_governance_guide |

Guide notebooks are located in `notebooks/guides/` (e.g., `notebooks/guides/lab_03_delta_dml_guide.ipynb`).

---

## Bonus Notebooks

| Notebook | Topic | Path |
|----------|-------|------|
| BONUS_aibi_dashboards | AI/BI Dashboards & Genie | `notebooks/bonus/BONUS_aibi_dashboards.ipynb` |
| BONUS_timestamps_autoloader_archive | Timestamps, UTC & Auto Loader Archiving | `notebooks/bonus/BONUS_timestamps_autoloader_archive.ipynb` |
| BONUS_advanced_transformations | SQL Transformations (JOINs, CTEs, Window Functions) | `notebooks/bonus/BONUS_advanced_transformations.ipynb` |
| BONUS_advanced_transformations_workshop | Transformations Workshop Lab | `notebooks/bonus/BONUS_advanced_transformations_workshop.ipynb` |
| BONUS_advanced_transformations_workshop_guide | Transformations Lab Guide | `notebooks/bonus/BONUS_advanced_transformations_workshop_guide.ipynb` |
| BONUS_powerbi_direct_query | Power BI Live Direct Query Demo | `notebooks/bonus/BONUS_powerbi_direct_query.ipynb` |

---

## Setup

Before running any notebook, run the setup notebook:

```
notebooks/setup/00_pre_config.ipynb   — run ONCE per workspace (admin)
notebooks/setup/00_setup.ipynb        — run automatically via %run
```

For external data connections (optional):
```
notebooks/bonus/BONUS_external_connection.ipynb
```

---

## Repository Structure

```
.
├── README.md
├── assets/
│   └── images/                       # Notebook images (107 files)
├── dataset/
│   ├── customers/                    # customers.csv, customers_new.csv
│   ├── orders/                       # orders_batch.json, stream/*.json
│   ├── products/                     # products.csv, products.parquet
│   ├── demo/                         # Additional demo stream files
│   └── workshop/                     # Workshop datasets (Lakeflow, AdventureWorks)
├── materials/
│   ├── lakeflow/                     # Lakeflow pipeline SQL/Python files
│   ├── medallion/                    # Medallion layer notebook tasks
│   └── orchestration/               # Job task scripts
└── notebooks/
    ├── setup/                        # Configuration notebooks
    ├── day1/
    │   ├── demo/                     # 00_intro → 03_delta_lake
    │   └── lab/                      # lab_01
    ├── day2/
    │   ├── demo/                     # 04_delta_optimization → 05_incremental_ingestion → 06_medallion_architecture
    │   └── lab/                      # lab_02, lab_05
    ├── day3/
    │   ├── demo/                     # 07_lakeflow_pipelines → 11_exam_preparation
    │   └── lab/                      # lab_07–lab_10
    ├── guides/                       # Trainer guide notebooks (lab_01, lab_03, lab_05, lab_07, lab_08, lab_10)
    └── bonus/                        # BONUS_aibi_dashboards, BONUS_timestamps, BONUS_advanced_transformations, BONUS_powerbi_direct_query
```

---

## Source Attribution

| Content | Source |
|---------|--------|
| Platform, Delta Lake, AI/BI | Databricks-Fundamental (DBF) |
| Optimization, Lakeflow, Governance | Databricks Lakehouse & Transformation (L&T) |
| Labs, Streaming, Transforms, Exam | Data Engineer Associate (DEA) |
| CI/CD lab, DENY privilege | Written from scratch |
