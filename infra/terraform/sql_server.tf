# ---------------------------------------------------------------------------
# Azure SQL - Lakeflow Connect CDC source (AdventureWorksLT sample)
# ---------------------------------------------------------------------------
# COST/TIER NOTE (do not "optimize" the SKU down):
#   CDC on Azure SQL Database requires >= S3 (DTU) or >= 1 vCore.
#   GP_S_Gen5_1 = General Purpose Serverless, 1 vCore max - the cheapest tier
#   that can still enable CDC, and it auto-pauses after 60 min idle (compute
#   billing drops to zero; storage pennies remain).
#   Cheaper alternative: CHANGE TRACKING works on any tier and is also
#   supported by Lakeflow Connect - see infra/sql/enable_cdc.sql.

resource "azurerm_mssql_server" "this" {
  name                         = local.sql_server_name
  resource_group_name          = azurerm_resource_group.this.name
  location                     = azurerm_resource_group.this.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_login
  administrator_login_password = var.sql_admin_password
  minimum_tls_version          = "1.2"

  tags = local.common_tags
}

resource "azurerm_mssql_database" "adventureworks" {
  name      = local.sql_database_name
  server_id = azurerm_mssql_server.this.id

  # Serverless General Purpose, 1 vCore - smallest CDC-capable SKU.
  sku_name                    = "GP_S_Gen5_1"
  min_capacity                = 0.5
  auto_pause_delay_in_minutes = 60
  max_size_gb                 = 4

  # Pre-load the AdventureWorksLT sample (SalesLT schema) at creation.
  sample_name = "AdventureWorksLT"

  # Sample DB, recreated on demand - no need for redundant backup storage.
  storage_account_type = "Local"

  tags = local.common_tags

  lifecycle {
    # sample_name is create-time only; ignore drift so re-plans stay clean.
    ignore_changes = [sample_name]
  }
}

# 0.0.0.0-0.0.0.0 is the Azure convention for "Allow Azure services and
# resources to access this server" - required for the Lakeflow Connect
# ingestion gateway running in Azure.
resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.this.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Trainer/classroom IPs. Accepts plain IPs or CIDRs; a CIDR is expanded to
# its first..last address range.
locals {
  trainer_ip_rules = {
    for idx, entry in var.trainer_ip_cidrs :
    format("trainer-%02d", idx) => {
      cidr  = can(regex("/", entry)) ? entry : "${entry}/32"
      bits  = can(regex("/", entry)) ? tonumber(split("/", entry)[1]) : 32
      start = cidrhost(can(regex("/", entry)) ? entry : "${entry}/32", 0)
    }
  }
}

resource "azurerm_mssql_firewall_rule" "trainer" {
  for_each = local.trainer_ip_rules

  name             = each.key
  server_id        = azurerm_mssql_server.this.id
  start_ip_address = each.value.start
  end_ip_address   = cidrhost(each.value.cidr, pow(2, 32 - each.value.bits) - 1)
}
