# Workflow Blueprint

This is the intended visual flow for the Foundry workflow designer.

```text
Start
  |
  v
Set variable: Local.user_question = System.LastMessage.Text
  |
  v
Invoke agent: crai-intake-router
Save output as: Local.route_result
  |
  v
If / else condition
  |
  +-- Local.route_result.route = "policy"
  |     |
  |     v
  |   Invoke agent: crai-policy-agent
  |   Save output as: Local.specialist_result
  |
  +-- Local.route_result.route = "loan_file"
  |     |
  |     v
  |   Invoke agent: crai-loan-file-agent
  |   Save output as: Local.specialist_result
  |
  +-- Local.route_result.route = "governance"
  |     |
  |     v
  |   Invoke agent: crai-governance-agent
  |   Save output as: Local.specialist_result
  |
  +-- Local.route_result.route = "human_review"
  |     |
  |     v
  |   Send message:
  |   "This request requires authorized human review. The assistant cannot approve,
  |   deny, price, or recommend a final loan decision."
  |
  +-- Else
        |
        v
      Send message:
      "This workflow handles credit policy, loan-file review, governance, and
      human-review routing for the synthetic credit-risk demo."

Specialist branches
  |
  v
Invoke agent: crai-response-synthesizer
  |
  v
Send final message
```

## Suggested Branch Conditions

```text
Local.route_result.route = "policy"
Local.route_result.route = "loan_file"
Local.route_result.route = "governance"
Local.route_result.route = "human_review"
```

## Suggested Variables

| Variable | Purpose |
| --- | --- |
| `Local.user_question` | Original user question |
| `Local.route_result` | Router JSON output |
| `Local.specialist_result` | Specialist JSON output |
| `Local.final_answer` | Synthesized answer |

