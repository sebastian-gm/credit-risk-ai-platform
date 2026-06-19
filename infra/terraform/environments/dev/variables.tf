variable "subscription_id" {
  description = "Azure subscription ID for this environment."
  type        = string
  default     = "778b05a9-6f2e-4809-a4f5-d2e29cfb9094"
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
