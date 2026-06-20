# Governance Plan

## AI Use-Case Registry

The structured AI use-case registry lives in:

```text
src/governance/ai_use_case_registry.csv
```

It tracks:

- use case ID
- name
- department
- owner
- business purpose
- risk level
- data sensitivity
- human review requirement
- production status
- demo approval
- primary control

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

## SQL Governance Tables

The SQL loader creates these governance tables:

```text
dbo.ai_use_case_registry
dbo.ai_tool_review_checklist
dbo.ai_prompt_library
dbo.ai_audit_log
```

These tables make the governance layer reportable in Power BI.

## Current Seeded Use Cases

```text
UC-001 Credit Policy Assistant: Medium risk, demo approved
UC-002 Loan File Summary: High risk, demo approved with human review
UC-003 Missing Document Detection: Medium risk, demo approved
UC-004 Invoice Field Extraction: Medium risk, demo approved
UC-005 Executive Portfolio Summary: Low risk, planned
UC-006 Fully Automated Loan Approval: Prohibited, blocked
```

## Tool Review Checklist

The checklist records whether each AI workflow has:

- grounding controls
- evaluation evidence
- human-review controls
- workflow routing controls
- validation controls
- acceptable-use review

The prohibited automated-loan-approval use case intentionally fails review and
is marked blocked. This demonstrates that the governance process can reject an
AI use case, not only approve demos.

## Prompt Library

The prompt library tracks prompt ID, associated use case, version, owner, risk
level, prompt purpose, allowed data, required controls, and lifecycle status.

The prompt library is intentionally metadata-only. Full prompts can be stored
separately if they become long or sensitive.

## Audit Log

The seed audit log captures representative AI activity:

- RAG query
- evaluation run
- invoice extraction
- blocked use-case review

Each event records sensitivity, output type, citation behavior, human-review
requirement, and outcome.

## Public Portfolio Rule

The public version of this project must clearly say:

```text
Demo case study built with synthetic data.
```
