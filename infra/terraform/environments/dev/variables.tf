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

variable "search_location" {
  description = "Azure region for Azure AI Search resources. Kept separate because Search capacity can differ by region."
  type        = string
  default     = "canadacentral"
}

variable "openai_location" {
  description = "Azure region for Azure OpenAI resources. Kept separate because model quota and availability vary by region."
  type        = string
  default     = "eastus2"
}

variable "document_intelligence_location" {
  description = "Azure region for Document Intelligence resources."
  type        = string
  default     = "eastus2"
}

variable "openai_chat_model_name" {
  description = "Chat model deployed for the demo assistant."
  type        = string
  default     = "gpt-5-mini"
}

variable "openai_chat_model_version" {
  description = "Chat model version deployed for the demo assistant."
  type        = string
  default     = "2025-08-07"
}

variable "openai_chat_deployment_name" {
  description = "Azure OpenAI deployment name used by the assistant scripts."
  type        = string
  default     = "gpt-5-mini"
}

variable "openai_chat_deployment_sku" {
  description = "Azure OpenAI deployment SKU."
  type        = string
  default     = "GlobalStandard"
}

variable "openai_chat_deployment_capacity" {
  description = "Azure OpenAI deployment capacity in thousands of tokens per minute."
  type        = number
  default     = 10
}

variable "openai_embedding_model_name" {
  description = "Embedding model deployed for vector retrieval."
  type        = string
  default     = "text-embedding-3-small"
}

variable "openai_embedding_model_version" {
  description = "Embedding model version deployed for vector retrieval."
  type        = string
  default     = "1"
}

variable "openai_embedding_deployment_name" {
  description = "Azure OpenAI deployment name used by embedding scripts."
  type        = string
  default     = "text-embedding-3-small"
}

variable "openai_embedding_deployment_sku" {
  description = "Azure OpenAI embedding deployment SKU."
  type        = string
  default     = "GlobalStandard"
}

variable "openai_embedding_deployment_capacity" {
  description = "Azure OpenAI embedding deployment capacity in thousands of tokens per minute."
  type        = number
  default     = 10
}

variable "document_intelligence_sku" {
  description = "Document Intelligence pricing tier. F0 is used for low-cost portfolio testing."
  type        = string
  default     = "F0"
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
