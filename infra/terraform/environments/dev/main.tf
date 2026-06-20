data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 6
  lower   = true
  upper   = false
  numeric = true
  special = false
}

resource "random_password" "sql_admin" {
  length           = 24
  special          = true
  override_special = "_%@"
}

locals {
  name_prefix          = "${var.project}-${var.environment}"
  region_code          = replace(var.location, " ", "")
  sql_region_code      = replace(var.sql_location, " ", "")
  search_region_code   = replace(var.search_location, " ", "")
  openai_region_code   = replace(var.openai_location, " ", "")
  docintel_region_code = replace(var.document_intelligence_location, " ", "")
  common_tags = merge(var.tags, {
    managed_by = "terraform"
  })
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${local.name_prefix}-${local.region_code}"
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = "law-${local.name_prefix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.common_tags
}

resource "azurerm_application_insights" "main" {
  name                = "appi-${local.name_prefix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
  tags                = local.common_tags
}

resource "azurerm_storage_account" "main" {
  name                     = "st${var.project}${var.environment}${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true
  min_tls_version          = "TLS1_2"
  tags                     = local.common_tags
}

resource "azurerm_storage_data_lake_gen2_filesystem" "raw" {
  name               = "raw"
  storage_account_id = azurerm_storage_account.main.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "processed" {
  name               = "processed"
  storage_account_id = azurerm_storage_account.main.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "curated" {
  name               = "curated"
  storage_account_id = azurerm_storage_account.main.id
}

resource "azurerm_key_vault" "main" {
  name                       = "kv-${local.name_prefix}-${random_string.suffix.result}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  rbac_authorization_enabled = true
  tags                       = local.common_tags
}

resource "azurerm_mssql_server" "main" {
  name                          = "sql-${local.name_prefix}-${local.sql_region_code}-${random_string.suffix.result}"
  resource_group_name           = azurerm_resource_group.main.name
  location                      = var.sql_location
  version                       = "12.0"
  administrator_login           = var.sql_admin_login
  administrator_login_password  = random_password.sql_admin.result
  minimum_tls_version           = "1.2"
  public_network_access_enabled = true
  tags                          = local.common_tags
}

resource "azurerm_mssql_firewall_rule" "client" {
  count            = var.client_ip_address == "" ? 0 : 1
  name             = "fw-client-loader"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = var.client_ip_address
  end_ip_address   = var.client_ip_address
}

resource "azurerm_mssql_database" "main" {
  name                        = "sqldb-${local.name_prefix}"
  server_id                   = azurerm_mssql_server.main.id
  sku_name                    = "GP_S_Gen5_1"
  min_capacity                = 0.5
  auto_pause_delay_in_minutes = 60
  max_size_gb                 = 1
  storage_account_type        = "Local"
  tags                        = local.common_tags
}

resource "azurerm_search_service" "main" {
  name                = "srch-${local.name_prefix}-${local.search_region_code}-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.search_location
  sku                 = "free"
  tags                = local.common_tags
}

resource "azurerm_cognitive_account" "openai" {
  name                          = "aoai-${local.name_prefix}-${local.openai_region_code}-${random_string.suffix.result}"
  location                      = var.openai_location
  resource_group_name           = azurerm_resource_group.main.name
  kind                          = "OpenAI"
  sku_name                      = "S0"
  custom_subdomain_name         = "aoai-${local.name_prefix}-${local.openai_region_code}-${random_string.suffix.result}"
  public_network_access_enabled = true
  local_auth_enabled            = true
  tags                          = local.common_tags
}

resource "azurerm_cognitive_deployment" "chat" {
  name                 = var.openai_chat_deployment_name
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = var.openai_chat_model_name
    version = var.openai_chat_model_version
  }

  sku {
    name     = var.openai_chat_deployment_sku
    capacity = var.openai_chat_deployment_capacity
  }
}

resource "azurerm_cognitive_deployment" "embeddings" {
  name                 = var.openai_embedding_deployment_name
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = var.openai_embedding_model_name
    version = var.openai_embedding_model_version
  }

  sku {
    name     = var.openai_embedding_deployment_sku
    capacity = var.openai_embedding_deployment_capacity
  }
}

resource "azurerm_cognitive_account" "document_intelligence" {
  name                          = "di-${local.name_prefix}-${local.docintel_region_code}-${random_string.suffix.result}"
  location                      = var.document_intelligence_location
  resource_group_name           = azurerm_resource_group.main.name
  kind                          = "FormRecognizer"
  sku_name                      = var.document_intelligence_sku
  public_network_access_enabled = true
  local_auth_enabled            = true
  tags                          = local.common_tags
}
