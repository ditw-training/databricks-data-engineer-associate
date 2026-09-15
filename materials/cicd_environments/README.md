# env_demo — one bundle, three environments

Trainer demo for **module 09a** (`notebooks/day3/demo/09a_dabs_environments.ipynb`): the same
Declarative Automation Bundle (formerly DABs) deployed to `dev`, `test` and `prod`, with every
environment-specific value coming from **targets + variables**.

| File | Purpose |
|---|---|
| `databricks.yml` | variables (`catalog`, `env_name`, `schema`, `schedule_pause_status`, `min_rows`) and targets `dev` / `test` / `prod` |
| `resources/env_demo_job.yml` | one job; all values via `${var.*}`; nightly schedule with a variable pause status |
| `src/show_environment.py` | task notebook: prints the parameters, runs a threshold "quality gate", appends a row to `<catalog>.<schema>.env_demo_runs` |

## What differs per target (verified live 2026-09-14, Databricks CLI v1.16.1)

| | dev | test | prod |
|---|---|---|---|
| `mode` | development | production | production |
| job name | `[dev <user>] env_demo_job` | `[test] env_demo_job` | `env_demo_job` |
| `root_path` | `.bundle/env_demo/dev` (user home) | `.bundle/env_demo/test` (user home) | `.bundle/env_demo/prod` (user home; SP home in real life) |
| schema | `dev_env_demo` | `test_env_demo` | `prod_env_demo` |
| schedule | PAUSED (dev mode) | PAUSED | **UNPAUSED** |
| `min_rows` | 1 | 100 | 1000 |

## Demo script (from this folder)

```bash
# 1) resolved configuration per target
databricks bundle validate -t dev  --var="catalog=retailhub_trainer"
databricks bundle validate -t prod --var="catalog=retailhub_trainer" -o json

# 2) overrides without editing YAML
databricks bundle validate -t dev --var="catalog=retailhub_trainer" --var="min_rows=5000" -o json
BUNDLE_VAR_min_rows=5000 databricks bundle validate -t dev --var="catalog=retailhub_trainer" -o json

# 3) deploy + run two environments (never deploy prod in class: schedule is UNPAUSED)
databricks bundle deploy -t dev  --var="catalog=retailhub_trainer"
databricks bundle deploy -t test --var="catalog=retailhub_trainer"
databricks bundle run    -t dev  --var="catalog=retailhub_trainer" env_demo_job
databricks bundle run    -t test --var="catalog=retailhub_trainer" env_demo_job

# 4) cleanup
databricks bundle destroy -t dev  --var="catalog=retailhub_trainer" --auto-approve
databricks bundle destroy -t test --var="catalog=retailhub_trainer" --auto-approve
```

Authenticate first (`databricks auth login --host <workspace-url> --profile TRAINING`, then add `-p TRAINING`
to the commands), as described in `../cicd/README.md`.

## Notes

- Pointing `root_path` at `/Workspace/Shared/...` makes `bundle validate` warn that the folder is writable by all
  users — a good talking point; production bundles use a restricted folder (the service principal's home).
- `bundle destroy` removes the jobs and bundle files, not the data: drop `retailhub_trainer.dev_env_demo` /
  `test_env_demo` with `DROP SCHEMA ... CASCADE` if you want a clean catalog.
