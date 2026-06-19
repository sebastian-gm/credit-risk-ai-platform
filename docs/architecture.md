# Architecture

## High-Level Flow

```text
Synthetic documents/data
        |
        v
Data Lake Gen2: raw zone
        |
        v
Azure Functions ingestion pipeline
        |
        +--> Azure SQL document registry and workflow tables
        |
        +--> Azure Document Intelligence extraction
        |
        v
Data Lake Gen2: processed/curated zones
        |
        v
Chunking + embeddings
        |
        v
Azure AI Search hybrid/vector index
        |
        v
Azure OpenAI / Azure AI Foundry assistants
        |
        +--> cited answers
        +--> workflow outputs
        +--> evaluation logs
        |
        v
Power BI dashboard
```

## Main Components

- **Data Lake Gen2:** stores raw, processed, and curated documents.
- **Azure SQL:** stores metadata, document registry, workflow state, governance records, and evaluation results.
- **Azure Functions:** runs ingestion, extraction, chunking, and workflow automation.
- **Azure Document Intelligence:** extracts structured fields from forms and loan documents.
- **Azure AI Search:** powers hybrid and vector search with citations.
- **Azure OpenAI / Azure AI Foundry:** powers assistants and evaluation workflows.
- **Key Vault:** stores secrets and connection references.
- **Managed Identity:** avoids hard-coded credentials.
- **Power BI:** reports business value, quality, adoption, and governance risk.

## Design Principle

The assistant supports analysts. It does not approve or reject loans.

