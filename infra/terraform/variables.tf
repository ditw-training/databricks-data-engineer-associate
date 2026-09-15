variable "prefix" {
  description = "Short lowercase prefix used in all resource names (e.g. 'dea')."
  type        = string
  default     = "dea"

  validation {
    condition     = can(regex("^[a-z0-9]{2,10}$", var.prefix))
    error_message = "prefix must be 2-10 lowercase alphanumeric characters (it is embedded in storage account / SQL server names)."
  }
}

variable "location" {
  description = "Azure region for all resources. Pick a region where Unity Catalog auto-provisions a metastore (any mainstream region works, e.g. westeurope, polandcentral)."
  type        = string
  default     = "westeurope"
}

variable "existing_resource_group_name" {
  description = "Deploy into this pre-existing resource group instead of creating rg-<prefix>-training. Resources still go to var.location (the RG's own region does not matter). Leave empty to create the RG."
  type        = string
  default     = ""
}

variable "azure_resource_provider_registrations" {
  description = "azurerm provider's automatic resource provider registration (\"core\", \"extended\", \"all\", \"none\", \"legacy\"). Use \"none\" when the identity is Owner only on a resource group - registering providers needs subscription scope."
  type        = string
  default     = "core"
}

variable "auto_delete_after" {
  description = "Date (YYYY-MM-DD) after which everything here is garbage — stamped as the 'auto-delete-after' tag so subscription cleanup jobs / humans know it is safe to destroy. Set it to the day after Day 3 of the training."
  type        = string
  default     = "2026-09-30"

  validation {
    condition     = can(regex("^\\d{4}-\\d{2}-\\d{2}$", var.auto_delete_after))
    error_message = "auto_delete_after must be a date in YYYY-MM-DD format."
  }
}

variable "owner" {
  description = "Owner tag value (trainer identifier, e.g. an email)."
  type        = string
  default     = "dea-trainer"
}

# ---------------------------------------------------------------------------
# Databricks workspace
# ---------------------------------------------------------------------------

variable "create_workspace" {
  description = "Create a new premium Databricks workspace (true) or reuse an existing one (false). New workspaces get a 14-day free DBU trial - schedule the training within it."
  type        = bool
  default     = true
}

variable "existing_workspace_host" {
  description = "Only when create_workspace = false: URL of the existing workspace, e.g. https://adb-1234567890123456.7.azuredatabricks.net. Leave empty otherwise."
  type        = string
  default     = ""
}

variable "existing_workspace_id" {
  description = "Only when create_workspace = false: Azure resource ID of the existing workspace. Leave empty otherwise."
  type        = string
  default     = ""
}

# ---------------------------------------------------------------------------
# Unity Catalog wiring
# ---------------------------------------------------------------------------

variable "configure_uc" {
  description = "Create Unity Catalog objects (storage credential, external location, grants) via the Databricks provider. Requires the `az login` identity to be a workspace admin and the workspace to be attached to a metastore (Azure auto-provisions one per region - do NOT create a metastore here)."
  type        = bool
  default     = true
}

variable "databricks_auth_type" {
  description = "Auth for the workspace-level Databricks provider. \"azure-cli\" (default) uses the `az login` identity. Use \"pat\" with DATABRICKS_TOKEN set to an AAD token (`az account get-access-token --subscription <id> --resource 2ff814a6-3304-4ab8-85cb-cd0e6f879c1d`) when the default az account belongs to another tenant."
  type        = string
  default     = "azure-cli"
}

variable "training_group" {
  description = "Databricks account/workspace group that receives ALL PRIVILEGES on the external location. Must already exist in the workspace."
  type        = string
  default     = "alt_trn_gr"
}

# ---------------------------------------------------------------------------
# Azure SQL (Lakeflow Connect source)
# ---------------------------------------------------------------------------

variable "create_sql_server" {
  description = "Create the Azure SQL server + AdventureWorksLT DB here. Set false when the Lakeflow Connect source lives elsewhere (e.g. Microsoft.Sql not registered on this subscription - see infra/LAKEFLOW_CONNECT_CONNECTION.md)."
  type        = bool
  default     = true
}

variable "sql_admin_login" {
  description = "Administrator login for the Azure SQL logical server."
  type        = string
  default     = "deatrainer"
}

variable "sql_admin_password" {
  description = "Administrator password for the Azure SQL logical server (8-128 chars, 3 of 4 character classes). Set it in terraform.tfvars or via TF_VAR_sql_admin_password - never commit it."
  type        = string
  sensitive   = true
}

variable "trainer_ip_cidrs" {
  description = "List of public IPv4 addresses/CIDRs allowed through the SQL server firewall (trainer laptop, training-room egress IP). Single IPs may be given with or without /32."
  type        = list(string)
  default     = []
}
