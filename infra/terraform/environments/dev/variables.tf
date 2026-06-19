variable "location" {
  description = "Azure region for the dev environment."
  type        = string
  default     = "canadacentral"
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
  }
}

