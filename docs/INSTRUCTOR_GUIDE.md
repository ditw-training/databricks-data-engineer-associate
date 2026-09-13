# Instructor Guide — Databricks Data Engineer Associate (3 Days)

Internal facilitator notes. Participants never see this file.

## 0. Day-before checklist

1. **Infrastructure:** `infra/terraform` → `terraform apply` (⚠️ coordinate timing — never during another training on the same subscription). Then run `infra/sql/create_login_master.sql` (against `master`, set the `lakeflow_connect` password first), `infra/sql/enable_cdc.sql` (against AdventureWorksLT) and the Databricks utility script + `lakeflowSetupChangeDataCapture` — see `infra/terraform/README.md`. Run `notebooks/setup/00_pre_config` (training group `alt_trn_gr` must be assigned to the workspace).
2. **Workspace:** SKU `trial` = Premium + 14-day free DBUs (the trial window must cover the training). Verify: serverless notebooks enabled, Lakeflow Connect SQL Server connector available (UC + serverless enabled, permission to create classic clusters for the gateway), web terminal availability (needed for the primary path of LAB 09).
3. **Pre-config:** run `notebooks/setup/00_pre_config.ipynb` (creates per-user catalogs `retailhub_<slug>`, schemas, volumes, datasets, grants). Edit `TRAINER_OVERRIDES` in `notebooks/setup/00_setup.ipynb` for this delivery.
4. **Smoke test:** run the "Smoke Test" section at the end of `00_pre_config` — PASS for every participant. Then run one lab per day end-to-end (suggested: lab_02, lab_05, lab_07) plus `databricks bundle validate -t dev` in `materials/cicd/`.
5. **Lakeflow Connect dry-run:** create the UC connection + ingestion pipeline once yourself (click **Validate** in the wizard; if it reports missing permissions or DDL support objects, follow `docs/ENG/lakeflow_connect_sqlserver_guide.pdf`); leave it in place — participants query the landed tables during the Day-1 demo.
6. **Costs:** SQL DB is serverless with 60-min auto-pause (first query after a pause takes ~1 min — warm it up before the demo). `terraform destroy` after Day 3.

## 1. Agenda — 6 h of content per day (360' net, breaks not included)

Example grid 09:00–16:00 with breaks 15' + 30' lunch + 15'. Shift break times freely — the minutes per block are what the plan is built on. The earlier plan (345' slots) ran ~405/440/450' in practice. In this plan **module 07 + lab_07 run on Day 2** (right after medallion) and **05a + lab_06 are self-study** (10-minute briefing on Day 2).

### Day 1 — Platform, Ingestion, Lakeflow Connect, Delta Lake (360')
| Time | Min | Block | Material |
|---|---|---|---|
| 09:00–09:20 | 20' | Welcome, RetailHub scenario, agenda, **environment smoke test** | `00_intro` |
| 09:20–10:05 | 45' | Platform: UC hierarchy, compute types & cost models, serverless, Spark basics (lazy evaluation, Spark UI) | `01_platform_and_workspace` |
| 10:05–10:30 | 25' | **Lab 01** — serverless notebook, UC, Volumes | `day1/lab/lab_01` |
| 10:30–10:45 | — | *Break* | |
| 10:45–11:30 | 45' | Ingestion: readers & schemas, `read_files()`, CTAS, JDBC, ingestion decision framework | `02_data_ingestion` |
| 11:30–12:15 | 45' | **Lab 02** — ingestion (CSV/JSON/Parquet, schemas, CTAS) | `day1/lab/lab_02` |
| 12:15–12:45 | — | *Lunch* | |
| 12:45–13:15 | 30' | **Lakeflow Connect** — managed SQL Server connector, CDC round-trip | `02a_lakeflow_connect_demo` |
| 13:15–14:15 | 60' | Delta Lake: DML & MERGE, history, time travel, RESTORE, VACUUM, managed vs external | `03_delta_lake` |
| 14:15–14:30 | — | *Break* | |
| 14:30–15:10 | 40' | **Lab 03** — Delta DML & time travel | `day1/lab/lab_03` |
| 15:10–15:35 | 25' | **Day-1 quiz** (Q1–20) + review | quiz PDF / `utilization/quiz/day1` |
| 15:35–16:00 | 25' | Buffer — lab catch-up, environment issues, Q&A | — |

### Day 2 — Optimization, Incremental Ingestion, Medallion, Lakeflow Pipelines (360')
| Time | Min | Block | Material |
|---|---|---|---|
| 09:00–09:10 | 10' | Recap of Day 1 | — |
| 09:10–09:20 | 10' | Transformations — **self-study briefing**: what to work through in `05a` + `lab_06` (exam objectives 3.1–3.5) and how to check yourself | `05a_transformations`, `lab_06` (self-study) |
| 09:20–10:05 | 45' | Optimization: OPTIMIZE/VACUUM, Liquid Clustering, `CLUSTER BY AUTO`, predictive optimization, deletion vectors, skew & AQE | `04_delta_optimization` |
| 10:05–10:40 | 35' | **Lab 04** — optimization benchmark | `day2/lab/lab_04` |
| 10:40–10:55 | — | *Break* | |
| 10:55–11:45 | 50' | Incremental ingestion: COPY INTO idempotency, Auto Loader (directory listing vs file events), schema evolution | `05_incremental_ingestion` |
| 11:45–12:30 | 45' | **Lab 05** — COPY INTO + Auto Loader | `day2/lab/lab_05` |
| 12:30–13:00 | — | *Lunch* | |
| 13:00–13:30 | 30' | Medallion architecture (bronze → silver → gold), gold objects | `06_medallion_architecture` |
| 13:30–14:15 | 45' | **Lakeflow Spark Declarative Pipelines**: ST vs MV, `STREAM()`, expectations, AUTO CDC — DEMO 1 condensed | `07_lakeflow_pipelines` + `materials/lakeflow/lakeflow_step_by_step` |
| 14:15–14:30 | — | *Break* | |
| 14:30–15:15 | 45' | **Lab 07** — build & run the RetailHub pipeline (Tasks 1–5) | `day3/lab/lab_07` |
| 15:15–15:40 | 25' | **Day-2 quiz** (Q21–40, incl. transformation questions) + review | quiz PDF / `utilization/quiz/day2` |
| 15:40–16:00 | 20' | Buffer — lab catch-up, Q&A | — |

### Day 3 — Jobs, CI/CD, Troubleshooting, Governance, Exam (360')
| Time | Min | Block | Material |
|---|---|---|---|
| 09:00–09:10 | 10' | Recap of Day 2 | — |
| 09:10–09:55 | 45' | Lakeflow Jobs: task types, DAG, triggers, retries, if/else, `for_each`, parameters & task values, run history | `08_job_orchestration` |
| 09:55–10:50 | 55' | **Lab 08** — multi-task job (Section 1 + Tasks A–E) | `day3/lab/lab_08` |
| 10:50–11:05 | — | *Break* | |
| 11:05–11:35 | 30' | CI/CD: Git folders flow, Declarative Automation Bundles, variables & targets, CLI | `09_cicd_and_automation` + `materials/cicd` |
| 11:35–12:10 | 35' | **Lab 09** — deploy RetailHub as a bundle (incl. Git folder step) | `day3/lab/lab_09_dabs` |
| 12:10–12:40 | — | *Lunch* | |
| 12:40–13:15 | 35' | **Troubleshooting exercise** — broken job (Tasks 1–5) | `day3/lab/lab_troubleshooting` + `materials/troubleshooting` |
| 13:15–13:55 | 40' | Governance: managed vs external (`SET MANAGED`), GRANT/REVOKE, masks & row filters, ABAC | `10_governance_and_security` |
| 13:55–14:10 | — | *Break* | |
| 14:10–14:50 | 40' | **Lab 10** — governance (Tasks 1–9) | `day3/lab/lab_10` |
| 14:50–15:35 | 45' | **Exam prep** — domains, traps, strategy + **Day-3 quiz** (Q41–68) with review | `11_exam_preparation`, quiz PDF Q41–68 |
| 15:35–16:00 | 25' | Buffer / final Q&A, feedback, teardown reminder | — |

### Time by exam domain (approx., in class)
| Domain (weight) | Minutes | Where |
|---|---|---|
| Platform (6%) | ~70' | 01, lab_01 |
| Ingestion & loading (21%) | ~215' | 02, lab_02, 02a, 05, lab_05 |
| Transformation & modeling (22%) | ~130' + **self-study** | 06, 07, lab_07, briefing · self-study: 05a, lab_06 |
| Lakeflow Jobs (16%) | ~100' | 08, lab_08 (+ job runs in lab_09, troubleshooting) |
| CI/CD (10%) | ~65' | 09, lab_09 |
| Troubleshooting & optimization (10%) | ~115' | 04, lab_04, lab_troubleshooting |
| Governance & security (15%) | ~80' | 10, lab_10 (+ managed vs external in 03) |
| Delta Lake fundamentals (cross-domain) | ~100' | 03, lab_03 |

⚠️ **Domain 3 is the largest exam domain.** Objectives 3.1–3.5 (cleaning, joins & unions, column/row manipulation, dedup & aggregates, tuning configs) live only in the self-study pair 05a + lab_06. Use the Day-2 briefing to set it as explicit homework, and use the Day-2 quiz (Q21–40) to check it. If the group has little SQL/PySpark experience, consider a 25–30' live "transformations essentials" block (joins, union, dedup, aggregates from 05a) taken from the Day-3 buffer and lab_08.

## 1a. In-class scope — what is skipped (self-study)

Sections below are marked **⏭️ Self-study** in the notebooks. None of them is needed by a lab.

| Module | Skip in class | Why |
|---|---|---|
| 01 | Databricks Assistant, PySpark-vs-SQL comparison, Spark architecture §4 Catalyst/AQE (1 sentence) | AQE returns in 04; comparison is in `pyspark_vs_sparksql.pdf` |
| 02 | *DataFrame Transformations (optional)* | Covered properly in 05a |
| 03 | Identity & generated columns, Delta log internals, Common Errors | Beyond Associate level |
| 05a + lab_06 | **Whole module and lab are self-study** (10-minute briefing on Day 2: scope = objectives 3.1–3.5, guide + solution + quiz Q21–40 to self-check) | Time; trainer's decision 2026-09-13 |
| 04 | *Performance Bottlenecks* demo — show only the skew signature (Query Profile / Spark UI) in 3 minutes | Troubleshooting lab covers diagnosis hands-on |
| 05 | *Lakeflow Connect (Informational)*; Error Handling in 5 minutes | Lakeflow Connect done in 02a |
| 06 | Notebook Modularity Pattern; AUTO CDC snippets only as a pointer to Day 3 | Covered in 07 |
| 07 | FLOW/backfill demo, duplicate PySpark declarations (show one), What's New, Section 2 & Section 3 UI demo (done in lab_07), legacy APPLY CHANGES (one sentence), **DEMO 3 metadata-driven → homework** | Time; UI build happens in the lab |
| 10 | Monitoring & Observability (system tables), Delta Sharing | Beyond exam |
| Labs | lab_02 bonus bug hunt; lab_07 Tasks 6–7; lab_troubleshooting Task 6 | Stretch for fast participants / homework |
| Bonus | `BONUS_03`, `BONUS_05`, `BONUS_troubleshooting`, `notebooks/bonus/*` | Homework |

## 2. Per-lab facilitator notes

- **lab_01:** serverless-first; classic-cluster creation is YOUR demo only. If someone lacks serverless, pair them up rather than debugging entitlements live.
- **lab_02:** contains an intentional bug-hunt bonus. Solutions in `notebooks/solution/`.
- **lab_05 / dataset quirk (teachable, not a bug):** `orders/stream/orders_stream_001.json` is byte-identical to the first 10k rows of `orders_batch.json`, and key `ORD00030000` repeats between stream_003/004 with a different payload. Use it to provoke the "why does my count differ?" discussion → dedup/MERGE motivation (picked up again in the self-study lab_06 window-dedup task).
- **lab_07:** the ~3% intentional nulls in `orders_batch.json` feed the expectations/quarantine task. Stagger pipeline starts (3–4 participants at a time) to avoid a serverless DBU burst.
- **Module 07 demos:** three levels — DEMO 1 `lakeflow_step_by_step` (build from scratch: checkpoints → SCD1/SCD2 → MV → expectations; run its `00_demo_driver.py` between updates; the FAIL step really fails the update — time-box ~3 min), DEMO 2 = `lakeflow_demo` (the LAB 07 stack), DEMO 3 `lakeflow_metadata_driven` (config table → dynamic graph; run `00_create_config_table.py` first; the "add a config row live" cell is the wow-moment; label it *beyond exam*). DEMO 3 is homework / fast-finisher material in the 360' plan — it does not gate any lab. Each folder's README has the walkthrough script.
- **lab_08:** the break-and-repair task needs YOU to set the failing parameter — instructions inside the lab.
- **lab_09:** primary path = web terminal / local CLI; fallback = trainer-driven deploy on the projector with participants editing YAML + verifying via SDK cells. Decide the morning of Day 3 based on the smoke test.
- **lab_troubleshooting:** create the 3-task job from `materials/troubleshooting/broken_job/` before the block (or let a fast participant do it). Faults: wrong volume path (task 1), exploding join + absurd shuffle partitions (task 2), missing dependency (task 3).
- **lab_07 in 45' (Day 2):** Section 1 + Tasks 1–5; show the Task 7 quarantine count yourself at the debrief. Start the pipelines before the Day-2 quiz if they are still running. **lab_08 (55') and lab_10 (40')** run in full on Day 3.
- **lab_10:** ABAC policy creation usually needs privileges participants don't have — keep it as your demo; participants do masks/row filters directly.
- **Quizzes:** answer keys are embedded at the bottom of each quiz — display only the question part when projecting. The Day-3 quiz (28 Q, PDF Q41–68) has no agenda slot — use it as homework or during exam prep.
- **Participant PDFs** (`docs/ENG/`, `docs/PL/` — hand out the language the group prefers): cheatsheet and `pyspark_vs_sparksql` on Day 1; `external_connection_guide` and `lakeflow_connect_sqlserver_guide` with the ADLS / Lakeflow Connect blocks; quiz, `exam_objectives_map` and `next_steps` at the end of Day 3. The quiz PDF contains the answer key on its last page. Rebuild after editing sources: `./scripts/build_pdfs.sh`.

## 3. Known risks & fallbacks

| Risk | Fallback |
|---|---|
| Lakeflow Connect connector unavailable / source unreachable | Screenshots/pre-recorded run in `02a`; keep the decision-framework discussion live |
| Web terminal disabled → no CLI for lab_09 | Trainer-driven deploy; participants verify via SDK cells |
| Serverless quota with N concurrent pipelines | Stagger runs; worst case one shared trainer pipeline |
| SQL DB auto-paused before the demo | Query it 5 min before the block |
| UI drift vs screenshots | Narrate live UI; screenshots are illustrative |

## 4. Teardown (after Day 3)

1. `terraform destroy` in `infra/terraform` (removes RG, storage, SQL, workspace if created).
2. If the workspace is kept: run the Cleanup section of `00_pre_config` to drop per-user catalogs; delete the Lakeflow Connect ingestion pipeline, gateway and connection (the gateway runs classic compute continuously) and bundle deployments.
