output "resource_group_name" {
  description = "Training resource group."
  value       = azurerm_resource_group.this.name
}

output "workspace_url" {
  description = "Databricks workspace URL (created or pre-existing)."
  value       = local.databricks_host
}

output "storage_account_name" {
  description = "ADLS Gen2 storage account backing the raw/external containers."
  value       = azurerm_storage_account.this.name
}

output "access_connector_id" {
  description = "Azure resource ID of the Databricks access connector (used by the UC storage credential)."
  value       = azurerm_databricks_access_connector.this.id
}

output "external_location_url" {
  description = "abfss:// URL of the Unity Catalog external location."
  value       = local.external_location_url
}

output "raw_container_url" {
  description = "abfss:// URL of the raw landing container (Auto Loader / COPY INTO exercises)."
  value       = "abfss://raw@${azurerm_storage_account.this.name}.dfs.core.windows.net/"
}

output "sql_server_fqdn" {
  description = "Fully qualified domain name of the Azure SQL logical server."
  value       = azurerm_mssql_server.this.fully_qualified_domain_name
}

output "sql_database_name" {
  description = "Name of the AdventureWorksLT sample database."
  value       = azurerm_mssql_database.adventureworks.name
}

output "lakeflow_connect_connection_summary" {
  description = "Values to paste into the Lakeflow Connect / UC connection UI (Catalog > External data > Connections > SQL Server). User is created by infra/sql/enable_cdc.sql."
  value = {
    host     = azurerm_mssql_server.this.fully_qualified_domain_name
    port     = 1433
    database = azurerm_mssql_database.adventureworks.name
    user     = "lakeflow_connect"
  }
}
