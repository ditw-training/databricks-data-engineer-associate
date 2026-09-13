# RetailHub Broken Job — trainer setup

Assets for **lab_troubleshooting** (Day 3). `broken_job/` contains three
deliberately broken task notebooks (Databricks source format):

| Task | File | Planted faults |
|---|---|---|
| 1 `ingest` | `task_ingest.py` | Wrong Volume path (`.../dataset/...` instead of `.../datasets/...`) → `PATH_NOT_FOUND`; after the path is fixed, the reader schema names two fields wrong (`client_id`, `amount_total` vs source `customer_id`, `total_amount`) → all-NULL columns → quality gate raises |
| 2 `transform` | `task_transform.py` | Join on `left(customer_id, 8)` — a low-cardinality truncated key → ~100× row explosion visible in shuffle/output-row metrics; `spark.sql.shuffle.partitions = 4000` → thousands of tiny tasks |
| 3 `publish` | `task_publish.py` | Reads `silver.ts_orders_final`, a table no upstream task creates (transform writes `ts_orders_enriched`); in the job DAG it depends only on `ingest`, not `transform` |

## 👨‍🏫 Deploy before the lab (Day 3 morning)

1. Import the three notebooks into the workspace (e.g.
   `/Workspace/Shared/retailhub_broken_job/`). The `.py` files are Databricks
   source format — import preserves cells.
2. Create a Lakeflow Job named **`retailhub_broken_job`** (serverless compute):
   - `ingest` → notebook `task_ingest`, parameter `catalog = retailhub_trainer`
   - `transform` → notebook `task_transform`, **depends on `ingest`**, same parameter
   - `publish` → notebook `task_publish`, **depends on `ingest` only**
     (this wrong edge is part of the exercise — do NOT wire it to `transform`)
3. Run the job once so a failed run exists in the run history: `ingest` fails
   on `PATH_NOT_FOUND`, `transform`/`publish` are skipped (upstream failed).
4. Grant participants **CAN VIEW** on the job so they can open the run
   history, the DAG, and the task error details.

Participants never edit these notebooks — they diagnose from the run UI and
fix *scratch copies* inside `notebooks/day3/lab/lab_troubleshooting.ipynb`,
writing `ts_*` tables into their own catalogs.

Equivalent Jobs API JSON skeleton if you prefer to script it
(`databricks jobs create --json @broken_job.json`); in the UI use
**Jobs & Pipelines → job → ⋮ → Edit as YAML** for the YAML form:

```json
{
  "name": "retailhub_broken_job",
  "max_concurrent_runs": 1,
  "tasks": [
    { "task_key": "ingest",
      "notebook_task": { "notebook_path": "/Workspace/Shared/retailhub_broken_job/task_ingest",
                         "base_parameters": { "catalog": "retailhub_trainer" } } },
    { "task_key": "transform",
      "depends_on": [ { "task_key": "ingest" } ],
      "notebook_task": { "notebook_path": "/Workspace/Shared/retailhub_broken_job/task_transform",
                         "base_parameters": { "catalog": "retailhub_trainer" } } },
    { "task_key": "publish",
      "depends_on": [ { "task_key": "ingest" } ],
      "notebook_task": { "notebook_path": "/Workspace/Shared/retailhub_broken_job/task_publish",
                         "base_parameters": { "catalog": "retailhub_trainer" } } }
  ]
}
```
