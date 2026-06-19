# Azure Subscription Decision

## Recommendation

Use a separate Azure subscription for this portfolio project.

Best option:

```text
Subscription: sub-veerda-ai-lab
Resource group: rg-crai-dev-eastus2
```

## Do Not Use

Do not use the SLP Nova production subscription for this project.

Reasons:

- SLP Nova is a real product with sensitive healthcare/child-data concerns.
- This project is a portfolio/demo workload.
- Mixing them creates confusing billing, security, governance, and cleanup risk.

## Personal vs Veerda

Use your personal Azure account if:

- you want fastest setup;
- this is mainly for AI-103 learning and portfolio;
- you do not yet have a separate Veerda business Azure setup.

Use a Veerda Azure subscription if:

- you want Veerda to become the public consulting/studio brand;
- you are comfortable separating billing and access there;
- you want the case study to sit naturally under the Veerda brand.

## Practical Default

Start with a new lab subscription under your personal control:

```text
Account: sebastian.sgm@outlook.com
Subscription: sub-veerda-ai-lab
Resource group: rg-crai-dev-eastus2
```

This keeps SLP Nova isolated while still letting the project support Veerda's future consulting/studio positioning.
