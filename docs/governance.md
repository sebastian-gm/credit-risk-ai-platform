# Governance Plan

## AI Use-Case Registry

Track:

- use_case_id
- name
- department
- owner
- business purpose
- risk level
- data sensitivity
- human review requirement
- production status

## Risk Levels

- low: summarization of public/internal docs
- medium: workflow support using synthetic or internal data
- high: sensitive data, regulated decisions, or customer-impacting workflows
- prohibited: fully automated credit approval or adverse action decisions

## Required Controls

- citations for knowledge answers
- source document tracking
- human-in-the-loop review
- prompt versioning
- evaluation set before release
- audit logs
- PII masking where possible
- no real lending decisions

## Public Portfolio Rule

The public version of this project must clearly say:

```text
Demo case study built with synthetic data.
```

