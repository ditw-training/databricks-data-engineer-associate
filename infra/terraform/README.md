# DEA Training Infrastructure (Terraform)

Provisions everything the 3-day Databricks Data Engineer Associate training needs on Azure:

| Resource | Purpose |
|---|---|
| Resource group `rg-<prefix>-training` | Single blast radius — one `terraform destroy` removes everything |
| ADLS Gen2 storage account (+ `raw`, `external` containers) | Auto Loader / COPY INTO landing zone, UC external location backing |
| Databricks access connector + `Storage Blob Data Contributor` role | Managed-identity bridge for Unity Catalog |
| Databricks workspace (premium, optional) | Training workspace — new workspaces get a **14-day free DBU trial** |
| UC storage credential + external location + grants (optional) | `LOCATION`-based exercises for the `dea-training` group |
| Azure SQL server + `AdventureWorksLT` DB (serverless `GP_S_Gen5_1`) | Lakeflow Connect CDC source (demo `02a_lakeflow_connect_demo`) |

> ### ⚠️ WARNING — shared subscription
> **Do not `terraform apply` during another training on this subscription — coordinate timing.**
> This config creates role assignments and firewall-open resources on the company subscription. Agree an apply/destroy window with whoever else is using it.

## Prerequisites

- Terraform >= 1.5, Azure CLI, `sqlcmd` (or Azure Data Studio) for the post-deploy script.
- `az login` to the training subscription; `az account set --subscription <id>` if you have several.
- Azure roles for the deploying identity:
  - **Contributor** — to create resources, **and**
  - **User Access Administrator** (or Owner) — the access-connector role assignment fails without it.
- For the Unity Catalog part (`configure_uc = true`): the same `az login` identity must be a **workspace admin** on the target workspace, and the `training_group` (default `dea-training`) must already exist there.
- **Do NOT create a metastore.** On Azure, Databricks auto-provisions one Unity Catalog metastore per region and attaches new workspaces automatically. This config only adds a storage credential + external location on top.

## Quickstart

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars   # edit: password, IPs, dates
terraform init
terraform plan
terraform apply
```

Fresh-workspace tip: the UC objects need the workspace to exist and you to be its admin. If the first full apply trips on the Databricks provider, run once with `configure_uc = false`, open the workspace URL (which makes your identity the first admin), then set `configure_uc = true` and apply again.

**Post-deploy — enable CDC** (values from `terraform output`):

```bash
sqlcmd -S $(terraform output -raw sql_server_fqdn) -d AdventureWorksLT \
       -U deatrainer -P '<sql_admin_password>' -i ../sql/enable_cdc.sql
```

Edit the `lakeflow_connect` placeholder password in the script first — that user (not the admin) goes into the Databricks connection.

**Lakeflow Connect UI steps** (summary; details in `notebooks/day1/demo/02a_lakeflow_connect_demo.ipynb`):

1. `terraform output lakeflow_connect_connection_summary` → host / port 1433 / database / user.
2. Workspace → **Catalog → External data → Connections → Create connection** → type **SQL Server**, paste host/port/user (`lakeflow_connect`) + the password you set in the script.
3. **Data ingestion → SQL Server connector** → pick the connection → this creates the **ingestion gateway** pipeline + a UC **staging volume**, then the **managed ingestion pipeline**.
4. Select `SalesLT.Customer`, `Product`, `SalesOrderHeader`, `SalesOrderDetail` → target a shared schema (e.g. `lakeflow_connect`) → run.
5. Verify: `SELECT count(*) FROM <catalog>.lakeflow_connect.customer;` then `UPDATE` a row in the source and re-run the pipeline to show CDC flowing.

Smoke test **the day before Day 1**: external location `LIST 'abfss://external@…'` from a notebook, `SELECT count(*) FROM SalesLT.Customer` through the connection, `EXEC sys.sp_cdc_help_change_data_capture` lists 4 tables.

## Cost guardrails

| Item | Setting | Effect |
|---|---|---|
| Databricks DBUs | New premium workspace ⇒ 14-day free trial | **Schedule the 3 training days inside the trial window** — DBUs ≈ free |
| Databricks compute | Use **serverless** SQL warehouses / jobs / pipelines | No idle VMs; serverless bills only while running (after the trial, serverless DBUs bill normally — keep pipelines small, stop what you demo) |
| Azure SQL | `GP_S_Gen5_1` serverless, `min_capacity 0.5`, auto-pause 60 min | Compute cost → 0 when idle; ~4 GB storage pennies. **CDC needs ≥ 1 vCore (or ≥ S3 DTU)** — this SKU is the cheapest that qualifies. Change Tracking (see `../sql/enable_cdc.sql`) works on any tier if you downgrade |
| SQL auto-pause caveat | First query after pause takes ~30–60 s to resume | Warm the DB before the demo slot |
| Storage | `Standard_LRS`, small sample data | Cents for 3 days |
| Everything | `auto-delete-after` tag + `terraform destroy` | Nothing lingers past Day 3 |

## Teardown

After Day 3:

```bash
terraform destroy
```

Everything lives in `rg-<prefix>-training` (plus the workspace's managed RG, deleted with it) — **nothing survives**. Verify with `az group list -o table | grep <prefix>` if you want belt and braces. Delete the Lakeflow Connect gateway/ingestion pipelines in the workspace UI first if you created them (they are UI-created, not Terraform-managed — on a destroyed workspace they die with it anyway).

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `AuthorizationFailed` creating the role assignment | Deploying identity lacks User Access Administrator/Owner. Have an admin grant it, or ask them to create the role assignment manually and `terraform import` it |
| Databricks provider `cannot configure azure-cli auth` / 403 on UC resources | `az login` identity is not a workspace admin, or the workspace was never opened (first login bootstraps the admin). Open the workspace URL once; or two-phase apply (`configure_uc = false` → `true`) |
| `storage credential ... metastore not found` | Workspace not attached to a metastore. Azure auto-attaches in supported regions on first login; check **Catalog** in the UI. Do not create a metastore via Terraform |
| `databricks_grants`: principal `dea-training` not found | Create the group first (workspace admin settings → Identity and access → Groups) or change `training_group` |
| Storage account / SQL server name taken | Names include a random suffix, so rare — `terraform taint random_string.suffix` and re-apply for a new suffix |
| `sp_cdc_enable_db` fails / not supported | DB below 1 vCore / S3 tier (someone changed the SKU), or you connected to `master`. Use `-d AdventureWorksLT`; keep `GP_S_Gen5_1`; or switch to the Change Tracking block in the script |
| `sqlcmd` login timeout | Your public IP is not in `trainer_ip_cidrs` (`curl -s ifconfig.me`, add, re-apply), or the serverless DB is resuming from pause — retry after ~1 min |
| Lakeflow Connect gateway cannot reach SQL | `AllowAzureServices` firewall rule must exist (Terraform creates it); check connection uses `lakeflow_connect` user and port 1433 |
| Re-plan shows changes on every run | Should not happen (plan is idempotent). If `sample_name` drifts, the `ignore_changes` lifecycle handles it — report anything else |
| Manual fallback | If Terraform is blocked entirely: `BONUS_external_connection.ipynb` documents the manual ADLS/UC path, and the SQL DB can be portal-provisioned with the AdventureWorksLT sample as last resort |

State is local (`terraform.tfstate`) — fine for a 3-day disposable stack; keep the folder until after `destroy`. Never commit `terraform.tfvars` or state files.
