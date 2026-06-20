variable "subscription_id" {
  description = "Azure subscription ID for this environment."
  type        = string
}

variable "location" {
  description = "Azure region for the dev environment."
  type        = string
  default     = "eastus2"
}

variable "project" {
  description = "Short project name used in Azure resource names."
  type        = string
  default     = "crai"
}

variable "environment" {
  description = "Environment name."
  type        = string
  default     = "dev"
}

variable "sql_admin_login" {
  description = "Azure SQL administrator login for the demo SQL server."
  type        = string
  default     = "craisqladmin"
}

variable "client_ip_address" {
  description = "Client public IPv4 address allowed through the Azure SQL firewall for local loading."
  type        = string
  default     = ""
}

variable "sql_location" {
  description = "Azure region for Azure SQL resources. Kept separate because SQL availability can differ by subscription."
  type        = string
  default     = "canadacentral"
}

variable "tags" {
  description = "Common Azure tags."
  type        = map(string)
  default = {
    project     = "credit-risk-ai-platform"
    environment = "dev"
    data        = "synthetic"
    purpose     = "portfolio"
    owner       = "sebastian-gm"
  }
}
