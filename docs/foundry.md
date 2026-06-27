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
| Hosted agent | `credit-policy-assistant` |
| Container registry | `crzopquhgqtxx6y.azurecr.io` |

## What This Adds

The earlier platform work proves the data, search, extraction, and governance layers. The Foundry project adds a dedicated place to test model behavior, agent workflows, and future evaluation runs using the same credit-risk scenario.

Current scope:

- Foundry account and project provisioned with infrastructure code.
- Application Insights and Log Analytics connected for monitoring.
- `gpt-5-mini` deployed to the Foundry account.
- Project endpoint tested through the Responses API.
- Hosted `credit-policy-assistant` agent deployed to Azure AI Foundry.
- Agent grounds answers with the existing Azure AI Search index `credit-risk-documents`.
- Azure AI Search allows Entra authentication and the hosted agent identity has `Search Index Data Reader`.
- Hosted agent smoke evaluation completed in Foundry with 2 passed, 0 failed.

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

## Hosted Agent

The hosted agent endpoint is:

```text
https://ai-account-dosuleocw4nxo.services.ai.azure.com/api/projects/crai-foundry-project/agents/credit-policy-assistant/endpoint/protocols/openai/responses?api-version=v1
```

The agent:

- receives questions through the Foundry Responses protocol;
- queries Azure AI Search using Entra authentication, not a committed Search key;
- sends retrieved policy snippets to `gpt-5-mini`;
- returns concise answers with source-path citations;
- refuses to approve, deny, price, or recommend final loan decisions.

Remote test question:

```text
What policy applies when debt-to-income is above 45%?
```

Remote test result:

```text
Applications with a debt-to-income ratio above 45% require an exception review.
Sources include policies/credit_policy_2026.md and underwriting memo citations.
```

Evidence:

- [Hosted agent invoke output](evidence/foundry/hosted-agent-invoke-output.txt)
- [Hosted agent playground screenshot](evidence/foundry/hosted-agent-playground.png)
- [Hosted agent evaluation results](evidence/foundry/hosted-agent-evaluation-results.md)
- [Hosted agent evaluation screenshot](evidence/foundry/hosted-agent-evaluation-report.png)
- [Foundry workflow design](foundry-workflows.md)

## Hosted Agent Evaluation

The hosted agent was evaluated in Azure AI Foundry with a two-case smoke dataset:

- debt-to-income exception review;
- automated loan approval refusal.

Result:

```text
2 passed
0 failed
0 errored
```

Criteria:

- relevance
- task adherence
- intent resolution
- indirect attack

Artifacts:

- Dataset: `foundry/src/credit-policy-assistant/.foundry/datasets/smoke-credit-policy.jsonl`
- Evaluation config: `foundry/src/credit-policy-assistant/.foundry/evaluators/hosted-agent-smoke.eval.yaml`
- Raw result export: `foundry/src/credit-policy-assistant/.foundry/results/hosted-agent-smoke-results.json`
- Screenshot: `docs/evidence/foundry/hosted-agent-evaluation-report.png`
