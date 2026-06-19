# Azure Subscription Decision

## Recommendation

Use a separate Azure subscription for this portfolio project.

Best option:

```text
Subscription: sub-veerda-ai-lab
Resource group: rg-crai-dev-eastus2
```

## Subscription Separation

Use a dedicated lab subscription if:

- you want fastest setup;
- this is mainly for AI-103 learning and portfolio;
- you want simple billing visibility;
- you want easy cleanup after screenshots and demos.

Avoid mixing this project with production workloads.

## Practical Default

Start with a new lab subscription:

```text
Subscription: sub-veerda-ai-lab
Resource group: rg-crai-dev-eastus2
```

This keeps the portfolio environment isolated from other Azure work.
