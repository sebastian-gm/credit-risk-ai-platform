output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "key_vault_name" {
  value = azurerm_key_vault.main.name
}

output "application_insights_name" {
  value = azurerm_application_insights.main.name
}

output "sql_server_fqdn" {
  value = azurerm_mssql_server.main.fully_qualified_domain_name
}

output "sql_database_name" {
  value = azurerm_mssql_database.main.name
}

output "sql_admin_login" {
  value = azurerm_mssql_server.main.administrator_login
}

output "sql_admin_password" {
  value     = random_password.sql_admin.result
  sensitive = true
}

output "search_service_name" {
  value = azurerm_search_service.main.name
}

output "search_service_endpoint" {
  value = "https://${azurerm_search_service.main.name}.search.windows.net"
}

output "openai_account_name" {
  value = azurerm_cognitive_account.openai.name
}

output "openai_endpoint" {
  value = azurerm_cognitive_account.openai.endpoint
}

output "openai_chat_deployment_name" {
  value = azurerm_cognitive_deployment.chat.name
}

output "openai_embedding_deployment_name" {
  value = azurerm_cognitive_deployment.embeddings.name
}

output "document_intelligence_account_name" {
  value = azurerm_cognitive_account.document_intelligence.name
}

output "document_intelligence_endpoint" {
  value = azurerm_cognitive_account.document_intelligence.endpoint
}
