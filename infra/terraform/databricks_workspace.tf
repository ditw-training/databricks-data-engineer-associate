# ---------------------------------------------------------------------------
# Databricks workspace (optional - var.create_workspace)
# ---------------------------------------------------------------------------
# COST NOTE: a brand-new workspace comes with a 14-day free DBU trial
# (premium features included) - schedule the 3 training days inside that
# window and the DBU side of the bill is ~zero. Azure infra (VMs for classic
# compute) still bills normally; prefer SERVERLESS compute, which bills per
# use only while queries/jobs run. See README.md for the cost guardrails.

resource "azurerm_databricks_workspace" "this" {
  count = var.create_workspace ? 1 : 0

  name                = local.workspace_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  # Premium is required for Unity Catalog; covered by the 14-day trial.
  sku                         = "premium"
  managed_resource_group_name = local.managed_rg_name

  tags = local.common_tags
}
