# Credit Risk Orchestrator Workflow

This folder defines the low-code Foundry workflow design for a visual multi-agent demo.

The workflow is meant to be built in the Microsoft Foundry workflow designer. It uses prompt agents and branching logic to route credit-risk questions to the right specialist path.

## Workflow Goal

Create a visual orchestration demo that shows how a lending team can route requests across policy review, loan-file review, governance review, and human-review messaging.

## Agents

| Agent | Purpose |
| --- | --- |
| `crai-intake-router` | Classifies the user request and returns a route as JSON |
| `crai-policy-agent` | Answers policy questions from trusted policy and underwriting context |
| `crai-loan-file-agent` | Reviews loan-file questions, missing documents, and risk flags |
| `crai-governance-agent` | Checks whether the requested AI use case is allowed, restricted, or blocked |
| `crai-response-synthesizer` | Combines route output and specialist output into one concise final response |

## Routes

| Route | When To Use |
| --- | --- |
| `policy` | Policy, DTI, eligibility, required documentation, or underwriting rules |
| `loan_file` | Missing documents, application review, applicant file summary |
| `governance` | AI use-case approval, acceptable use, risk level, review controls |
| `human_review` | Any request asking the system to approve, deny, price, or recommend a loan decision |
| `unsupported` | Anything outside the credit-risk demo scope |

## Demo Questions

Use these in the Foundry workflow preview:

```text
What policy applies when debt-to-income is above 45%?
```

Expected route: `policy`

```text
Can the assistant approve a loan automatically?
```

Expected route: `human_review`

```text
What controls are required before releasing a credit policy assistant?
```

Expected route: `governance`

```text
What should an analyst check when a loan file is missing bank statements?
```

Expected route: `loan_file`

## Foundry Build Steps

1. Open Microsoft Foundry.
2. Open project `crai-foundry-project`.
3. Turn on `New Foundry`.
4. Go to `Build`.
5. Select `Create new workflow`.
6. Start with a blank or sequential workflow.
7. Create the five prompt agents listed above.
8. Use the prompts and JSON schemas in this folder.
9. Save the router output as `Local.route_result`.
10. Add an if/else node using the route values:

```text
Local.route_result.route = "policy"
Local.route_result.route = "loan_file"
Local.route_result.route = "governance"
Local.route_result.route = "human_review"
```

11. Route each branch to the matching specialist agent.
12. Send all successful specialist outputs to `crai-response-synthesizer`.
13. For `human_review`, return a message that final credit decisions require authorized human review.
14. Preview the four demo questions.
15. Capture screenshots of the visual workflow and preview output.

## Important Limitation

The workflow designer does not support hosted agents directly. The existing `credit-policy-assistant` hosted agent remains the production-style coded agent. This visual workflow uses prompt agents so the portfolio can show low-code orchestration, routing, branching, and traceable multi-agent behavior.

## Evidence To Capture

Save screenshots under:

```text
docs/evidence/foundry/
```

Recommended filenames:

```text
workflow-orchestrator-visual.png
workflow-policy-preview.png
workflow-human-review-preview.png
workflow-governance-preview.png
```

