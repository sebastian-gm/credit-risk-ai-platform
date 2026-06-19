# Azure Naming And Setup

## Recommended Subscription

Create a new subscription dedicated to portfolio and learning workloads.

Recommended subscription name:

```text
sub-veerda-ai-lab
```

Why:

- separates this project from SLP Nova production infrastructure;
- keeps billing and cleanup simple;
- supports future Veerda case studies and demos;
- avoids mixing portfolio experiments with sensitive product workloads.

Alternative names:

```text
sub-ai-portfolio
sub-credit-risk-ai
sub-veerda-labs
```

## Recommended Resource Groups

Start with one development resource group:

```text
rg-crai-dev-canadacentral
```

Future environments:

```text
rg-crai-stg-canadacentral
rg-crai-prod-canadacentral
```

For now, only create `dev`.

## Naming Prefix

Use:

```text
crai
```

Meaning:

```text
credit risk AI
```

## Initial Region

Recommended:

```text
Canada Central
```

Reason:

- close to your current operating context;
- already familiar from other Azure work;
- good default for learning and portfolio work.

If Azure OpenAI / AI Foundry model capacity is unavailable, use a supported alternate region for AI services while keeping the core data resources in Canada Central.

## Initial Azure Resources

Phase 1 creates:

- Resource Group
- Storage Account with Data Lake Gen2
- Data Lake filesystems: `raw`, `processed`, `curated`
- Key Vault
- Log Analytics Workspace
- Application Insights

Later phases add:

- Azure SQL
- Azure Functions
- Azure AI Document Intelligence
- Azure AI Search
- Azure OpenAI / Azure AI Foundry
- Power BI assets

## Tags

Apply these tags to all resources:

```text
project = credit-risk-ai-platform
environment = dev
data = synthetic
purpose = portfolio
owner = sebastian-gm
managed_by = terraform
```

## Budget Control

Create a monthly Azure budget before deploying AI services.

Recommended starting budget:

```text
CAD 50-100/month
```

Use alerts at:

```text
50%
80%
100%
```

## Required Information Before Deployment

Confirm:

- Azure account email
- Tenant ID
- Subscription ID
- Subscription name
- Region
- Monthly budget limit
- Whether GitHub Actions OIDC should be configured now or later

