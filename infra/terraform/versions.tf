terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "azurerm" {
  resource_provider_registrations = var.azure_resource_provider_registrations

  features {
    resource_group {
      # The Databricks managed RG contains auto-created resources; allow destroy.
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Workspace-level Databricks provider. Uses the Azure CLI identity (`az login`).
# That identity must be a WORKSPACE ADMIN for the UC resources (databricks_uc.tf).
# Only exercised when var.configure_uc = true.
provider "databricks" {
  alias     = "workspace"
  host      = local.databricks_host
  auth_type = var.databricks_auth_type
  # Pins the az token to the workspace's subscription/tenant, so it works even
  # when the default `az account` points at another subscription.
  azure_workspace_resource_id = local.workspace_id
}
