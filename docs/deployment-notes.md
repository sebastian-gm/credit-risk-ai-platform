# Deployment Notes

## Dev Foundation

Deployment date:

```text
2026-06-19
```

Subscription:

```text
Lab subscription
```

Tenant:

```text
Project tenant
```

Region:

```text
East US 2
```

Budget:

```text
budget-crai-dev
CAD 50 monthly
Alerts: 50%, 80%, 100%
```

Created resources:

```text
Resource group: rg-crai-dev-eastus2
Storage account: stcraidev6fecno
Data Lake filesystems: raw, processed, curated
Uploaded raw dataset path: raw/synthetic/
Uploaded processed registry path: processed/document_registry/
Key Vault: kv-crai-dev-6fecno
Log Analytics: law-crai-dev
Application Insights: appi-crai-dev
```

Current scope:

- low-cost Azure foundation only;
- no Azure OpenAI deployment yet;
- no Azure AI Search deployment yet;
- no Document Intelligence deployment yet;
- no real data.

Screenshot targets:

- resource group overview;
- storage account containers/filesystems;
- Key Vault overview;
- Log Analytics workspace overview;
- Application Insights overview;
- subscription budget page.
