# Lakeflow Connect → Azure SQL: manual connection checklist

What to enter in the Databricks UI to connect Lakeflow Connect to the training Azure SQL database
(`AdventureWorksLT`). The connection is created **manually** (not by Terraform).

> ⚠️ This repository is public — never commit passwords or real host names here.
> The real values live in `terraform output` and in the local, git-ignored `infra/terraform/terraform.tfvars`.

## 1. Before you start (once per deployment)

| Check | How |
|---|---|
| Azure SQL exists | `terraform -chdir=infra/terraform output sql_server_fqdn` |
| Firewall lets Databricks in | Rule `AllowAzureServices` (0.0.0.0) — created by Terraform |
| Login `lakeflow_connect` exists | `infra/sql/create_login_master.sql` run against `master` (sets the password) |
| CDC + DB user + grants | `infra/sql/enable_cdc.sql` run against `AdventureWorksLT` — only needed for the **CDC connector** |
| DDL support objects | Databricks `utility_script.sql` + `lakeflowSetupChangeDataCapture` — only for the **CDC connector** (see `infra/terraform/README.md`) |
| Your Databricks privileges | `CREATE CONNECTION` on the metastore (workspace/metastore admin has it) |

## 2. Create the Unity Catalog connection

**Catalog → Connect (External data) → Connections → Create connection**
(or **+ Create connection** inside the Data Ingestion wizard).

| Field | Value | Where to get it |
|---|---|---|
| Connection name | `retailhub_sqlserver` | fixed — notebooks and guides use this name |
| Connection type | **SQL Server** | |
| Auth type (if the form asks) | Username and password | |
| Host | `sql-dea-training-<suffix>.database.windows.net` | `terraform output -raw sql_server_fqdn` |
| Port | `1433` | |
| User | `lakeflow_connect` | **not** the admin `deatrainer` |
| Password | the `lakeflow_connect` password | set in `create_login_master.sql`; kept locally as a comment in `terraform.tfvars` |
| Trust server certificate (if shown) | leave **off** (default) | Azure SQL has a valid public certificate |

Then **Test connection → Create**. Verify in SQL: `SHOW CONNECTIONS; DESCRIBE CONNECTION retailhub_sqlserver;`

The database is **not** part of the connection — you pick it in the ingestion wizard
(source catalog = `AdventureWorksLT`, schema = `SalesLT`).

## 3a. Ingestion pipeline — CDC connector (with gateway)

**Data Ingestion → SQL Server**, choose connection `retailhub_sqlserver`.

| Wizard field | Value |
|---|---|
| Ingestion pipeline name | `retailhub_sqlserver_ingestion` |
| Event log catalog / schema | `retailhub_trainer` / `lakeflow_connect` |
| Ingestion gateway name | `retailhub_sqlserver_gateway` |
| Staging location | `retailhub_trainer` / `lakeflow_staging` |
| Source tables | `AdventureWorksLT` → `SalesLT` → `Customer`, `Product`, `SalesOrderHeader`, `SalesOrderDetail` |
| Destination | `retailhub_trainer` / `lakeflow_connect` |
| Database setup | **Validate** → must pass |
| Schedule | none (press **Start** during the demo) |

Cost: the gateway runs **continuously on classic compute (2 VMs)** and keeps the serverless SQL DB awake.
Create it ~15 min before the demo (VM start ≈ 8 min, snapshot ≈ 2 min) and **delete gateway + pipeline right after**.

## 3b. Ingestion pipeline — query-based connector (no gateway)

Same connection, no CDC, no gateway, no staging volume; serverless only. Changes are detected with a
**cursor column** (`ModifiedDate` exists in all four `SalesLT` tables).

**Data Ingestion → SQL Server**, choose connection `retailhub_sqlserver`, query-based ingestion.

| Wizard field | Value |
|---|---|
| Ingestion pipeline name | `retailhub_sqlserver_query_based` |
| Destination catalog | `retailhub_trainer` |
| Source tables | `AdventureWorksLT` → `SalesLT` → the four tables above |
| Cursor column (each table) | `ModifiedDate` |
| Destination schema | `retailhub_trainer` / `lakeflow_query` |
| Schedule | none (press **Start** during the demo) |

Change round-trip: an `UPDATE` is picked up only if it moves the cursor, e.g.
`UPDATE SalesLT.Customer SET Phone = '555-TRAINING-42', ModifiedDate = GETUTCDATE() WHERE CustomerID = 1;`
Hard deletes are not captured by default.

## 4. Let participants read the result

```sql
GRANT USE CATALOG ON CATALOG retailhub_trainer TO `alt_trn_gr`;
GRANT USE SCHEMA, SELECT ON SCHEMA retailhub_trainer.lakeflow_connect TO `alt_trn_gr`;  -- or lakeflow_query
```

## 5. Troubleshooting

| Symptom | Fix |
|---|---|
| Test connection times out | Serverless DB resuming from auto-pause (30–60 s) — retry; check `AllowAzureServices` firewall rule |
| `Login failed for user 'lakeflow_connect'` | Wrong password, or `create_login_master.sql` not run against `master` |
| Gateway validation reports missing objects/permissions | Run `enable_cdc.sql` and the Databricks utility script (`lakeflowSetupChangeDataCapture`, `lakeflowFixPermissions`) |
| Gateway stuck in `WAITING_FOR_RESOURCES` | Classic VMs are starting (≈ 8 min in westus3) — check vCPU quota if it lasts longer |
