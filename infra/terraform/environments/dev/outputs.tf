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
