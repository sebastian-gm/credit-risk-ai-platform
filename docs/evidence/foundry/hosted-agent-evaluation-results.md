# Hosted Agent Evaluation Results

Evaluation run completed on June 21, 2026.

## Scope

This smoke evaluation checks the deployed Foundry hosted agent against two credit-policy questions:

- debt-to-income exception review;
- automated loan approval refusal.

The goal is to confirm that the hosted agent answers from the policy corpus, follows the approval boundary, and avoids unsafe final credit decisions.

## Foundry Run

| Item | Value |
| --- | --- |
| Agent | `credit-policy-assistant` |
| Agent version | `1` |
| Evaluation | `eval_2fc26565c77547bea4fa18abf67d5147` |
| Run | `evalrun_644e9dae5742461e950d53fd64d42129` |
| Status | `completed` |
| Result | `2 passed, 0 failed, 0 errored` |

## Criteria

| Criterion | Passed | Failed | Errored |
| --- | ---: | ---: | ---: |
| relevance | 2 | 0 | 0 |
| task_adherence | 2 | 0 | 0 |
| intent_resolution | 2 | 0 | 0 |
| indirect_attack | 2 | 0 | 0 |

## Local Artifacts

- Dataset: `foundry/src/credit-policy-assistant/.foundry/datasets/smoke-credit-policy.jsonl`
- Evaluation config: `foundry/src/credit-policy-assistant/.foundry/evaluators/hosted-agent-smoke.eval.yaml`
- Raw result export: `foundry/src/credit-policy-assistant/.foundry/results/hosted-agent-smoke-results.json`
- Screenshot: [hosted-agent-evaluation-report.png](hosted-agent-evaluation-report.png)

## Interpretation

The hosted agent passed the first smoke evaluation. This is not a full production benchmark. It is a focused portfolio check showing that the Foundry-hosted assistant can be evaluated for answer relevance, instruction following, intent handling, and resistance to unsafe prompt behavior.
