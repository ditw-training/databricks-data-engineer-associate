# RetailHub — Declarative Automation Bundle

A working **Declarative Automation Bundle** (formerly *Databricks Asset Bundles / DABs*)
for the RetailHub capstone. It packages two resources:

| Resource | File | What it is |
|---|---|---|
| `retailhub_pipeline` | `resources/retailhub_pipeline.yml` | Lakeflow Spark Declarative Pipeline over the star-schema SQL sources in `../lakeflow/lakeflow_demo/transformations/` (serverless, triggered) |
| `retailhub_job` | `resources/retailhub_job.yml` | 3-task Lakeflow Job: validate (notebook) → refresh pipeline (pipeline task) → report (notebook), serverless compute |

Used by **lab_09_dabs** (Day 3) and the live deploy demo in `09_cicd_and_automation`.

## Bundle anatomy

```
materials/cicd/                      <- bundle root (run all commands from here)
├── databricks.yml                   <- bundle name, variables, targets, sync paths
├── resources/
│   ├── retailhub_pipeline.yml       <- pipelines: retailhub_pipeline
│   └── retailhub_job.yml            <- jobs: retailhub_job
└── README.md

referenced sources (outside the bundle root, added via sync.paths):
../lakeflow/lakeflow_demo/transformations/**   <- pipeline SQL (bronze/silver/gold)
../orchestration/task_01_validate.py           <- job task 1 (notebook source)
../orchestration/task_03_report.py             <- job task 3 (notebook source)
```

Key concepts to point at while reading `databricks.yml`:

- **`bundle.name`** — namespace for everything the bundle deploys.
- **`include`** — pulls the `resources/*.yml` files into the configuration.
- **`sync.paths`** — the pipeline SQL and task notebooks live *outside*
  `materials/cicd/`; listing `../lakeflow/lakeflow_demo` and `../orchestration`
  here makes `bundle deploy` upload them too.
- **`variables`** — `catalog` (your personal `retailhub_<slug>` catalog) and
  `schema_prefix` (pipeline publishes to `<catalog>.<schema_prefix>_lakeflow`).
- **`targets`** — `dev` (default, `mode: development`) plus a commented `prod`
  stub for the dev-vs-prod discussion.
- **Relative paths** in a resource YAML resolve **relative to the file that
  declares them** — that is why `resources/*.yml` use `../../lakeflow/...`
  while this README talks about `../lakeflow/...` (relative to the bundle root).
- **Resource references** — the job binds to the pipeline with
  `${resources.pipelines.retailhub_pipeline.id}`; the CLI substitutes the real
  pipeline id at deploy time, so the two resources stay wired together in
  every target.

## Prerequisites

- Databricks CLI **v0.230+** (`databricks --version`) — the new Go CLI, not the
  legacy `databricks-cli` pip package.
- Authentication configured (below).
- Your personal training catalog exists (`retailhub_<slug>` from `00_pre_config`).

## Authentication — via profile

```bash
# One-time: OAuth login, stored as a named profile in ~/.databrickscfg
databricks auth login --host https://adb-XXXXXXXXXXXXXXXX.XX.azuredatabricks.net --profile TRAINING

# Check what the profile resolves to
databricks auth describe --profile TRAINING
```

Then either pass `-p TRAINING` on every command or `export DATABRICKS_CONFIG_PROFILE=TRAINING`.
In the **workspace web terminal** authentication is inherited — no profile needed.

## Commands

Run from `materials/cicd/` (the folder containing `databricks.yml`):

```bash
# 1. Validate — parse config, resolve variables/paths, print the plan summary
databricks bundle validate -t dev --var="catalog=retailhub_<your_slug>"

# 2. Deploy — upload synced files + create/update the pipeline and the job
databricks bundle deploy -t dev --var="catalog=retailhub_<your_slug>"

# 3. Run the job (waits and streams task states until a terminal state)
databricks bundle run -t dev --var="catalog=retailhub_<your_slug>" retailhub_job

# Inspect the rendered config / deployment summary
databricks bundle summary -t dev --var="catalog=retailhub_<your_slug>"

# Tear down everything the bundle created in this target
databricks bundle destroy -t dev --var="catalog=retailhub_<your_slug>"
```

With `-t dev` (`mode: development`) the deployed resources are named
**`[dev <your user name>] retailhub_job`** / **`[dev <your user name>] retailhub_pipeline`**,
schedules and triggers are paused, and files land under
`/Workspace/Users/<you>/.bundle/retailhub/dev/`. Every participant can therefore
deploy their own isolated copy of the same code.

## Notes

- `--var="catalog=..."` overrides the `catalog` variable (default:
  `retailhub_trainer`). Without it you would deploy against the trainer catalog
  and likely fail on permissions — always pass your own catalog.
- The two notebook tasks intentionally run against `samples.nyctaxi.trips` so
  the job succeeds on any workspace; the pipeline task builds the RetailHub
  star schema in `<catalog>.<schema_prefix>_lakeflow`. Re-pointing the
  validate/report tasks at RetailHub tables is a stretch exercise in lab_09.
- The `prod` target is a commented stub in `databricks.yml` — used only for
  the dev-vs-prod reflection task, not deployed during the training.
