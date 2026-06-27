# Azure AI Foundry Workflows

This project includes a planned visual workflow in Microsoft Foundry:

```text
Credit Risk Orchestrator
```

The workflow shows how credit-risk requests can be routed across specialized agents with if/else logic, variables, structured JSON outputs, and preview traces.

## Why This Matters

The hosted `credit-policy-assistant` proves the coded agent path. The workflow adds a low-code orchestration path that is easier to show in a portfolio demo because reviewers can see the routing graph.

## Workflow Scope

The workflow routes questions to:

- credit policy review;
- loan-file review;
- AI governance review;
- human-review messaging for prohibited final-decision requests.

## Design Files

- [Workflow README](../foundry/workflows/credit-risk-orchestrator/README.md)
- [Workflow blueprint](../foundry/workflows/credit-risk-orchestrator/workflow-blueprint.md)
- [Agent prompts](../foundry/workflows/credit-risk-orchestrator/agent-prompts.md)
- [JSON schemas](../foundry/workflows/credit-risk-orchestrator/json-schemas.md)

## Current Implementation Note

Microsoft Foundry workflow designer is portal/VS Code Toolkit driven. The available Azure Developer CLI in this environment manages hosted agents, but it does not provide a workflow creation command.

The next implementation step is to build the workflow in the Foundry visual designer using the design files above, then save screenshots under:

```text
docs/evidence/foundry/
```

## Demo Evidence To Capture

| Evidence | Purpose |
| --- | --- |
| `workflow-orchestrator-visual.png` | Shows the visual routing graph |
| `workflow-policy-preview.png` | Shows the policy path working |
| `workflow-human-review-preview.png` | Shows final loan decisions are blocked |
| `workflow-governance-preview.png` | Shows governance routing and controls |

## Microsoft References

- [Build a workflow in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow)
- [Add declarative agent workflows in Visual Studio Code](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/vs-code-agents-workflow-low-code)
