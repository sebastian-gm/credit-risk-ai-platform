# Foundry Project Evidence

Provisioned on June 20, 2026.

## Resource Group

```text
rg-crai-foundry-dev-eastus2
```

Screenshot:

- [foundry-resource-group-overview.png](foundry-resource-group-overview.png)

## Resources Created

```text
Name                                           Kind        Location
---------------------------------------------  ----------  ----------
ai-account-dosuleocw4nxo                       AIServices  eastus2
logs-dosuleocw4nxo                                         eastus2
ai-account-dosuleocw4nxo/crai-foundry-project  AIServices  eastus2
appi-dosuleocw4nxo                             web         eastus2
```

## Project Endpoint

```text
https://ai-account-dosuleocw4nxo.services.ai.azure.com/api/projects/crai-foundry-project
```

## Model Deployment

```text
Name        Model       Version     State    Sku             Capacity    AgentsV2    Responses
----------  ----------  ----------  -------  --------------  ----------  ----------  -----------
gpt-5-mini  gpt-5-mini  2025-08-07  Running  GlobalStandard  10          true        true
```

## Endpoint Test

Prompt:

```text
In one sentence, explain what a credit policy assistant does for a lending analyst. Mention that it supports review but does not make final loan decisions.
```

Response:

```text
A credit policy assistant supports a lending analyst by summarizing relevant policies, identifying compliance issues and risk flags, and suggesting documentation and checks to streamline the review--while the analyst retains responsibility for final loan decisions.
```

Result:

```text
status: completed
model: gpt-5-mini
project route: /api/projects/crai-foundry-project/openai/v1/responses
```
