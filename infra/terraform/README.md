# Terraform

Terraform scaffold for the Azure foundation.

## Environments

```text
infra/terraform/environments/dev
```

## First Deployment Target

The first deployment should create:

- resource group
- storage account with Data Lake Gen2 enabled
- Log Analytics workspace
- Application Insights
- Key Vault

Azure SQL, Azure AI Search, Document Intelligence, and Azure OpenAI should be added after the subscription and region are confirmed.

## Usage

```bash
cd infra/terraform/environments/dev
terraform init
terraform plan
```

Do not run `terraform apply` until the Azure subscription is confirmed.

