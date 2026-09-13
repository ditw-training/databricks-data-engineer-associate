# ---------------------------------------------------------------------------
# ADLS Gen2 storage + Unity Catalog access connector
# ---------------------------------------------------------------------------

resource "azurerm_storage_account" "this" {
  name                     = local.storage_account_name
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS" # cheapest replication - training data is disposable
  account_kind             = "StorageV2"
  is_hns_enabled           = true # ADLS Gen2 (hierarchical namespace) - required for abfss:// / UC

  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false

  tags = local.common_tags
}

# Landing zone for raw files (Auto Loader / COPY INTO exercises).
resource "azurerm_storage_container" "raw" {
  name                  = "raw"
  storage_account_id    = azurerm_storage_account.this.id
  container_access_type = "private"
}

# Backing container for the Unity Catalog external location.
resource "azurerm_storage_container" "external" {
  name                  = "external"
  storage_account_id    = azurerm_storage_account.this.id
  container_access_type = "private"
}

# Managed identity bridge between Unity Catalog and the storage account.
resource "azurerm_databricks_access_connector" "this" {
  name                = local.access_connector_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  identity {
    type = "SystemAssigned"
  }

  tags = local.common_tags
}

# Requires the deploying identity to hold User Access Administrator (or Owner)
# on the subscription/RG - plain Contributor cannot create role assignments.
resource "azurerm_role_assignment" "connector_storage" {
  scope                = azurerm_storage_account.this.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_databricks_access_connector.this.identity[0].principal_id
}
