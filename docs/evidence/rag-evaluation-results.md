# RAG Evaluation Results

## Summary

- Cases: 4
- Retrieval hit rate @5: 1.00
- Answer non-empty rate: 1.00
- Answer term pass rate: 1.00
- Mean reciprocal rank: 0.88
- All cases passed: True

## Cases

### dti_exception_policy

Question: What policy applies when debt-to-income is above 45%?

Expected citation rank: 1
Retrieval hit @5: True
Answer non-empty: True
Answer term pass: True

Retrieved citations:

- raw/synthetic/policies/credit_policy_2026.md
- raw/synthetic/underwriting_memos/APP-2026-0001_memo.md
- raw/synthetic/underwriting_memos/APP-2026-0006_memo.md
- raw/synthetic/underwriting_memos/APP-2026-0004_memo.md
- raw/synthetic/underwriting_memos/APP-2026-0003_memo.md

Answer:

```text
Applications with a debt-to-income ratio above 45% require exception review. (Source: raw/synthetic/policies/credit_policy_2026.md; see also raw/synthetic/underwriting_memos/APP-2026-0004_memo.md)
```

### small_business_required_documents

Question: What documents are required for small-business loans?

Expected citation rank: 1
Retrieval hit @5: True
Answer non-empty: True
Answer term pass: True

Retrieved citations:

- raw/synthetic/policies/document_checklist_policy.md
- raw/synthetic/loan_applications/APP-2026-0005.json
- raw/synthetic/underwriting_memos/APP-2026-0005_memo.md
- raw/synthetic/loan_applications/APP-2026-0002.json
- raw/synthetic/underwriting_memos/APP-2026-0002_memo.md

Answer:

```text
Required documents for small-business loans:
- completed application form
- business bank-statement summary
- business tax return or owner income support
- ownership attestation
- compliance checklist

Source: raw/synthetic/policies/document_checklist_policy.md

(Policy also states missing required documents should route the file to Operations before final analyst review. Source: raw/synthetic/policies/document_checklist_policy.md)
```

### missing_document_detection

Question: Where should missing required documents be routed?

Expected citation rank: 2
Retrieval hit @5: True
Answer non-empty: True
Answer term pass: True

Retrieved citations:

- raw/synthetic/fraud_notes/address_mismatch_review.md
- raw/synthetic/policies/document_checklist_policy.md
- raw/synthetic/compliance/manual_review_checklist.md
- raw/synthetic/operations/weekly_credit_ops_report.md
- raw/synthetic/policies/fair_lending_policy.md

Answer:

```text
Missing required documents should be routed to Operations before final analyst review. (raw/synthetic/policies/document_checklist_policy.md)
```

### prohibited_automation

Question: Can the AI assistant approve or deny a loan automatically?

Expected citation rank: 1
Retrieval hit @5: True
Answer non-empty: True
Answer term pass: True

Retrieved citations:

- raw/synthetic/compliance/ai_use_case_registry.md
- raw/synthetic/policies/credit_policy_2026.md
- raw/synthetic/policies/fair_lending_policy.md
- raw/synthetic/underwriting_memos/APP-2026-0003_memo.md
- raw/synthetic/compliance/manual_review_checklist.md

Answer:

```text
No. Fully automated loan approval or denial is prohibited — the AI may summarize and cite policy/documents but must not make final credit decisions. See:

- raw/synthetic/compliance/ai_use_case_registry.md ("Prohibited use: Fully automated loan approval, denial, pricing, or adverse action generation.")
- raw/synthetic/policies/credit_policy_2026.md ("the AI assistant... must not approve, reject, or price a loan. Final decisions require an authorized human analyst.")
- raw/synthetic/policies/fair_lending_policy.md ("Prohibited uses: - automated final approval or denial; ... Required controls: human-in-the-loop review;")
- raw/synthetic/underwriting_memos/APP-2026-0003_memo.md ("AI may summarize this file and cite policy sections, but final credit decisions require human analyst review.")
- raw/synthetic/compliance/manual_review_checklist.md ("no final decision is made solely from AI output.")
```
