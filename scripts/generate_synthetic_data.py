#!/usr/bin/env python3
"""Generate synthetic credit-risk portfolio data for the demo project."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "synthetic"


APPLICATIONS = [
    {
        "application_id": "APP-2026-0001",
        "applicant_name": "Maya Torres",
        "product": "Personal Loan",
        "requested_amount": 18500,
        "annual_income": 72000,
        "credit_score": 704,
        "dti": 0.31,
        "employment_months": 48,
        "state": "FL",
        "channel": "Digital",
        "risk_band": "B",
        "status": "manual_review",
        "missing_docs": "none",
        "synthetic_pii": "yes",
    },
    {
        "application_id": "APP-2026-0002",
        "applicant_name": "Evan Brooks",
        "product": "Small Business Loan",
        "requested_amount": 65000,
        "annual_income": 118000,
        "credit_score": 681,
        "dti": 0.42,
        "employment_months": 22,
        "state": "GA",
        "channel": "Broker",
        "risk_band": "C",
        "status": "manual_review",
        "missing_docs": "bank_statement_q2",
        "synthetic_pii": "yes",
    },
    {
        "application_id": "APP-2026-0003",
        "applicant_name": "Nadia Chen",
        "product": "Personal Loan",
        "requested_amount": 9200,
        "annual_income": 54000,
        "credit_score": 742,
        "dti": 0.24,
        "employment_months": 61,
        "state": "TX",
        "channel": "Digital",
        "risk_band": "A",
        "status": "ready_for_decision",
        "missing_docs": "none",
        "synthetic_pii": "yes",
    },
    {
        "application_id": "APP-2026-0004",
        "applicant_name": "Leo Martin",
        "product": "Personal Loan",
        "requested_amount": 27800,
        "annual_income": 63000,
        "credit_score": 626,
        "dti": 0.49,
        "employment_months": 15,
        "state": "AZ",
        "channel": "Digital",
        "risk_band": "D",
        "status": "exception_review",
        "missing_docs": "income_verification",
        "synthetic_pii": "yes",
    },
    {
        "application_id": "APP-2026-0005",
        "applicant_name": "Sofia Alvarez",
        "product": "Small Business Loan",
        "requested_amount": 42000,
        "annual_income": 96000,
        "credit_score": 713,
        "dti": 0.36,
        "employment_months": 39,
        "state": "FL",
        "channel": "Partner",
        "risk_band": "B",
        "status": "manual_review",
        "missing_docs": "business_tax_return",
        "synthetic_pii": "yes",
    },
    {
        "application_id": "APP-2026-0006",
        "applicant_name": "Owen Patel",
        "product": "Personal Loan",
        "requested_amount": 31500,
        "annual_income": 85000,
        "credit_score": 658,
        "dti": 0.45,
        "employment_months": 27,
        "state": "NC",
        "channel": "Digital",
        "risk_band": "C",
        "status": "fraud_review",
        "missing_docs": "address_verification",
        "synthetic_pii": "yes",
    },
]


def write_text(relative_path: str, content: str) -> None:
    path = OUT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def write_csv(relative_path: str, rows: list[dict[str, object]]) -> None:
    path = OUT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(relative_path: str, payload: object) -> None:
    path = OUT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def generate() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    write_text(
        "README.md",
        """
        # Synthetic Credit Risk Dataset

        This dataset is fully synthetic and created for the Credit Risk AI Platform demo.
        It does not contain real applicants, real customers, real lenders, or credit-bureau data.

        The data is designed to support:

        - document ingestion;
        - metadata classification;
        - Azure Document Intelligence extraction;
        - Azure AI Search indexing;
        - RAG answers with citations;
        - governance and evaluation examples;
        - Power BI reporting.
        """,
    )

    write_csv("structured/loan_applications.csv", APPLICATIONS)

    write_csv(
        "structured/portfolio_performance.csv",
        [
            {"month": "2026-01", "applications": 820, "approval_rate": 0.42, "avg_decision_hours": 18.4, "chargeoff_rate": 0.031, "manual_review_rate": 0.33},
            {"month": "2026-02", "applications": 870, "approval_rate": 0.44, "avg_decision_hours": 17.1, "chargeoff_rate": 0.029, "manual_review_rate": 0.31},
            {"month": "2026-03", "applications": 910, "approval_rate": 0.41, "avg_decision_hours": 20.2, "chargeoff_rate": 0.034, "manual_review_rate": 0.36},
            {"month": "2026-04", "applications": 945, "approval_rate": 0.43, "avg_decision_hours": 19.0, "chargeoff_rate": 0.033, "manual_review_rate": 0.34},
            {"month": "2026-05", "applications": 990, "approval_rate": 0.45, "avg_decision_hours": 16.8, "chargeoff_rate": 0.030, "manual_review_rate": 0.29},
        ],
    )

    write_csv(
        "structured/document_registry_seed.csv",
        [
            {"document_id": "DOC-POL-001", "file_path": "policies/credit_policy_2026.md", "document_type": "policy", "department": "Credit Risk", "sensitivity_label": "internal", "owner": "credit_policy"},
            {"document_id": "DOC-POL-002", "file_path": "policies/fair_lending_policy.md", "document_type": "policy", "department": "Compliance", "sensitivity_label": "internal", "owner": "compliance"},
            {"document_id": "DOC-POL-003", "file_path": "policies/document_checklist_policy.md", "document_type": "policy", "department": "Operations", "sensitivity_label": "internal", "owner": "loan_ops"},
            {"document_id": "DOC-RPT-001", "file_path": "operations/weekly_credit_ops_report.md", "document_type": "operations_report", "department": "Operations", "sensitivity_label": "internal", "owner": "loan_ops"},
        ],
    )

    write_text(
        "policies/credit_policy_2026.md",
        """
        # LumaCredit Credit Policy 2026

        ## Purpose

        This policy defines underwriting guidance for personal loans and small-business loans.
        All examples are synthetic.

        ## Minimum Review Standards

        Applications with a credit score below 640 require manual review.
        Applications with debt-to-income ratio above 45% require exception review.
        Applications with employment history below 18 months require additional income verification.
        Requested amount should be reasonable compared with verified income and existing obligations.

        ## Risk Bands

        - Band A: strong credit profile, low DTI, complete documentation.
        - Band B: acceptable profile with minor review notes.
        - Band C: moderate risk requiring analyst review.
        - Band D: high risk requiring exception approval.

        ## Human Review

        The AI assistant may summarize files and policy evidence, but it must not approve,
        reject, or price a loan. Final decisions require an authorized human analyst.
        """,
    )

    write_text(
        "policies/fair_lending_policy.md",
        """
        # Fair Lending And Responsible AI Policy

        LumaCredit requires consistent review standards across applicants and channels.
        Analysts must not use protected-class attributes in credit decisions.
        AI-generated summaries must include citations when referencing policy or applicant documents.

        Prohibited uses:

        - automated final approval or denial;
        - adverse action language generated without human review;
        - hidden scoring logic that cannot be explained;
        - use of real personal data in public demos or model tests.

        Required controls:

        - human-in-the-loop review;
        - source citation tracking;
        - audit log for AI-assisted workflows;
        - synthetic data for public portfolio examples;
        - periodic evaluation of groundedness and refusal behavior.
        """,
    )

    write_text(
        "policies/document_checklist_policy.md",
        """
        # Loan File Document Checklist Policy

        Required documents for personal loans:

        - completed application form;
        - income verification;
        - identity verification;
        - address verification when mismatch signals are present;
        - bank-statement summary for larger requests.

        Required documents for small-business loans:

        - completed application form;
        - business bank-statement summary;
        - business tax return or owner income support;
        - ownership attestation;
        - compliance checklist.

        Missing required documents should route the file to Operations before final analyst review.
        """,
    )

    write_text(
        "operations/weekly_credit_ops_report.md",
        """
        # Weekly Credit Operations Report

        Reporting week: 2026-06-12

        Application volume increased 8% from the prior week. Manual-review queues are concentrated
        in small-business loan files with missing bank-statement summaries. Average decision time
        improved for digital personal-loan applications but worsened for broker-channel exceptions.

        Key issues:

        - 17% of small-business files are missing one or more required documents.
        - Exception-review files with DTI above 45% have the longest queue time.
        - Fraud review volume increased because of address-verification mismatches.

        Recommended actions:

        - prioritize missing-document detection at intake;
        - create analyst checklist summaries for Band C and Band D files;
        - add weekly governance review for AI-assisted risk memo drafts.
        """,
    )

    for app in APPLICATIONS:
        application_id = app["application_id"]
        write_json(
            f"loan_applications/{application_id}.json",
            {
                "notice": "Synthetic demo record. Not real applicant data.",
                **app,
                "declared_purpose": "debt consolidation" if app["product"] == "Personal Loan" else "working capital",
                "income_source": "employment" if app["product"] == "Personal Loan" else "business revenue",
                "documents_received": ["application_form", "identity_verification", "income_verification"],
                "analyst_queue": app["status"],
            },
        )
        write_text(
            f"underwriting_memos/{application_id}_memo.md",
            f"""
            # Underwriting Memo: {application_id}

            Applicant: {app["applicant_name"]}
            Product: {app["product"]}
            Requested amount: ${app["requested_amount"]:,}
            Credit score: {app["credit_score"]}
            Debt-to-income ratio: {app["dti"]:.0%}
            Employment history: {app["employment_months"]} months
            Risk band: {app["risk_band"]}

            ## Analyst Notes

            This synthetic file is currently marked as `{app["status"]}`.
            Missing documents: {app["missing_docs"]}.

            ## Policy Considerations

            Files below 640 credit score require manual review.
            Files above 45% DTI require exception review.
            Files below 18 months of employment history require additional income verification.

            ## AI Use Boundary

            AI may summarize this file and cite policy sections, but final credit decisions require
            human analyst review.
            """,
        )

    write_text(
        "fraud_notes/address_mismatch_review.md",
        """
        # Fraud Review Note: Address Mismatch Queue

        Several synthetic applications show address-verification mismatches between the application
        form and supporting documents. These records should be routed to Fraud / Risk Ops before
        final underwriting.

        Review triggers:

        - address verification missing;
        - inconsistent state between applicant profile and document metadata;
        - broker-channel submissions with incomplete ownership attestation;
        - repeated contact details across unrelated synthetic applications.
        """,
    )

    write_text(
        "compliance/ai_use_case_registry.md",
        """
        # AI Use-Case Registry

        | Use Case | Department | Risk Level | Human Review | Status |
        |---|---|---:|---|---|
        | Credit Policy Assistant | Credit Risk | Medium | Required | Demo |
        | Loan File Summary | Credit Risk | High | Required | Demo |
        | Missing Document Detection | Operations | Medium | Required | Demo |
        | Executive Portfolio Summary | Leadership | Low | Recommended | Demo |

        Prohibited use:

        Fully automated loan approval, denial, pricing, or adverse action generation.
        """,
    )

    write_text(
        "compliance/manual_review_checklist.md",
        """
        # Manual Review Checklist

        Analysts should confirm:

        - all required documents are present;
        - extracted income fields match supporting documents;
        - DTI and requested amount are reasonable;
        - exception-review reasons are documented;
        - AI-generated content includes source citations;
        - no final decision is made solely from AI output.
        """,
    )


if __name__ == "__main__":
    generate()
