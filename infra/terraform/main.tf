# ---------------------------------------------------------------------------
# Naming, tags, resource group
# ---------------------------------------------------------------------------

# Short random suffix to keep globally-unique names (storage account, SQL
# server) collision-free across repeated create/destroy cycles.
resource "random_string" "suffix" {
  length  = 5
  lower   = true
  upper   = false
  numeric = true
  special = false
}

locals {
  suffix = random_string.suffix.result

  resource_group_name = "rg-${var.prefix}-training"

  # Storage account: lowercase alphanumeric, max 24 chars, globally unique.
  storage_account_name = substr("st${var.prefix}training${local.suffix}", 0, 24)

  access_connector_name = "dbac-${var.prefix}-training"
  workspace_name        = "dbw-${var.prefix}-training"
  managed_rg_name       = "rg-${var.prefix}-training-dbw-managed"

  sql_server_name   = "sql-${var.prefix}-training-${local.suffix}"
  sql_database_name = "AdventureWorksLT"

  # Resolved workspace endpoints (created vs. pre-existing).
  databricks_host = var.create_workspace ? "https://${azurerm_databricks_workspace.this[0].workspace_url}" : var.existing_workspace_host
  workspace_id    = var.create_workspace ? azurerm_databricks_workspace.this[0].id : var.existing_workspace_id

  external_location_url = "abfss://external@${azurerm_storage_account.this.name}.dfs.core.windows.net/"

  common_tags = {
    project           = "databricks-dea-training"
    environment       = "training"
    owner             = var.owner
    managed-by        = "terraform"
    auto-delete-after = var.auto_delete_after
  }
}

# Soft guard: reusing a workspace requires its host + id.
check "existing_workspace_inputs" {
  assert {
    condition     = var.create_workspace || (var.existing_workspace_host != "" && var.existing_workspace_id != "")
    error_message = "create_workspace = false requires both existing_workspace_host and existing_workspace_id."
  }
}

resource "azurerm_resource_group" "this" {
  name     = local.resource_group_name
  location = var.location
  tags     = local.common_tags
}
