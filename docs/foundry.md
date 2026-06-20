# Azure AI Foundry Setup

This project includes a separate Azure AI Foundry project for model and agent testing.

## Resources

| Item | Value |
| --- | --- |
| Subscription | `sub-veerda-ai-lab` |
| Resource group | `rg-crai-foundry-dev-eastus2` |
| Foundry account | `ai-account-dosuleocw4nxo` |
| Foundry project | `crai-foundry-project` |
| Region | `eastus2` |
| Project endpoint | `https://ai-account-dosuleocw4nxo.services.ai.azure.com/api/projects/crai-foundry-project` |
| Model deployment | `gpt-5-mini` |

## What This Adds

The earlier platform work proves the data, search, extraction, and governance layers. The Foundry project adds a dedicated place to test model behavior, agent workflows, and future evaluation runs using the same credit-risk scenario.

Current scope:

- Foundry account and project provisioned with infrastructure code.
- Application Insights and Log Analytics connected for monitoring.
- `gpt-5-mini` deployed to the Foundry account.
- Project endpoint tested through the Responses API.

Run the endpoint smoke test:

```bash
python3 scripts/test_foundry_responses_endpoint.py
```

## Endpoint Note

The working route for model calls is the Foundry project endpoint:

```text
https://ai-account-dosuleocw4nxo.services.ai.azure.com/api/projects/crai-foundry-project/openai/v1/responses
```

The direct account endpoint is not the preferred route for this Foundry project setup.

## Next Foundry Step

The next useful step is a small Credit Policy Assistant in Foundry that uses the existing Azure AI Search index as its grounding source. That will connect the current RAG work to a visible Foundry agent experience.
