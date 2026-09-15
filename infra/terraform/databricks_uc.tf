# ---------------------------------------------------------------------------
# Unity Catalog wiring (optional - var.configure_uc)
# ---------------------------------------------------------------------------
# Do NOT create a metastore here: on Azure, Databricks auto-provisions one
# metastore per region and attaches new workspaces to it. These resources
# only wire the workspace's existing metastore to our ADLS Gen2 container.
#
# The `az login` identity must be a WORKSPACE ADMIN (and metastore admin or
# owner of the created objects for the grants to succeed).

resource "databricks_storage_credential" "external" {
  count    = var.configure_uc ? 1 : 0
  provider = databricks.workspace

  name    = "sc-${var.prefix}-training-adls"
  comment = "DEA training - managed identity of the access connector (Terraform-managed)"

  azure_managed_identity {
    access_connector_id = azurerm_databricks_access_connector.this.id
  }

  # Training infra is disposable - allow destroy even if dependents linger.
  force_destroy = true

  depends_on = [azurerm_role_assignment.connector_storage]
}

resource "databricks_external_location" "external" {
  count    = var.configure_uc ? 1 : 0
  provider = databricks.workspace

  name            = "el-${var.prefix}-training-external"
  url             = local.external_location_url
  credential_name = databricks_storage_credential.external[0].name
  comment         = "DEA training - external tables / LOCATION exercises (Terraform-managed)"

  force_destroy = true
}

resource "databricks_grants" "external_location" {
  count    = var.configure_uc ? 1 : 0
  provider = databricks.workspace

  external_location = databricks_external_location.external[0].id

  grant {
    principal  = var.training_group
    privileges = ["ALL_PRIVILEGES"]
  }
}
