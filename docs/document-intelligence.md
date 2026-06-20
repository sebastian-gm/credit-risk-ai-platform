# Document Intelligence

Azure AI Document Intelligence extracts structured fields from business
documents. The first demo uses the prebuilt invoice model against a synthetic
invoice PDF.

## Configuration

```text
Resource kind: FormRecognizer
Pricing tier: F0
Model ID: prebuilt-invoice
API version: 2024-11-30
Input: synthetic PDF invoice
Contains real data: false
```

## Run

Generate the synthetic invoice:

```bash
python3 src/extraction/create_synthetic_invoice_pdf.py
```

Analyze the invoice:

```bash
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="https://<document-intelligence-resource>.cognitiveservices.azure.com/" \
AZURE_DOCUMENT_INTELLIGENCE_KEY="<document-intelligence-key>" \
python3 scripts/analyze_invoice_document.py
```

The script writes:

```text
data/processed/document_intelligence/synthetic_invoice_raw.json
data/processed/document_intelligence/synthetic_invoice_summary.json
```

These output files are local generated artifacts and are not committed.

## Portfolio Value

This milestone demonstrates:

- prebuilt document extraction;
- async Azure AI service calls;
- field normalization from model output;
- invoice automation use case for Finance/Ops;
- safe handling of synthetic documents only.

## Smoke Test

Synthetic invoice:

```text
data/processed/extraction_samples/synthetic_invoice_lumacredit.pdf
```

Observed fields:

```text
VendorName: Northstar Office Supplies
CustomerName: LumaCredit Finance Operations
InvoiceId: INV-2026-1042
InvoiceDate: 2026-06-15
DueDate: 2026-07-15
SubTotal: USD 1,525.00
TotalTax: USD 106.75
InvoiceTotal: USD 1,631.75
Status: succeeded
```

Current limitation:

```text
The simple generated PDF extracted header and total fields correctly, but did
not extract line items as structured invoice items. A more realistic invoice
template or scanned sample should be added before demonstrating line-item
automation.
```
