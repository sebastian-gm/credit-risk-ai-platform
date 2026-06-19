# Source Code

Python code will be organized by pipeline stage:

```text
src/ingestion/      # file registration and metadata extraction
src/extraction/     # Document Intelligence clients and validators
src/search/         # chunking, embeddings, and Azure AI Search indexing
src/assistants/     # RAG orchestration and prompt templates
src/evaluation/     # golden question sets and scoring
src/shared/         # shared config, logging, and models
```

