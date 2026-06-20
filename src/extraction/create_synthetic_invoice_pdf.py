#!/usr/bin/env python3
"""Create a small synthetic invoice PDF for Document Intelligence testing."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed" / "extraction_samples" / "synthetic_invoice_lumacredit.pdf"

INVOICE_LINES = [
    "INVOICE",
    "Vendor: Northstar Office Supplies",
    "Vendor Address: 100 Harbor Street, Miami, FL 33131",
    "Bill To: LumaCredit Finance Operations",
    "Customer Address: 250 Brickell Avenue, Miami, FL 33131",
    "Invoice Number: INV-2026-1042",
    "Invoice Date: 2026-06-15",
    "Due Date: 2026-07-15",
    "",
    "Description                         Quantity   Unit Price   Amount",
    "Document scanning service                 1      450.00      450.00",
    "Secure file storage                       3       75.00      225.00",
    "Workflow automation setup                 1      850.00      850.00",
    "",
    "Subtotal: USD 1,525.00",
    "Tax: USD 106.75",
    "Invoice Total: USD 1,631.75",
    "",
    "Payment Terms: Net 30",
    "Remit To: ap@northstar.example",
    "Synthetic document for portfolio testing. Contains no real customer data.",
]


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_content_stream() -> bytes:
    lines = ["BT", "/F1 12 Tf", "50 760 Td", "16 TL"]
    for idx, line in enumerate(INVOICE_LINES):
        if idx:
            lines.append("T*")
        lines.append(f"({escape_pdf_text(line)}) Tj")
    lines.append("ET")
    return "\n".join(lines).encode("ascii")


def build_pdf() -> bytes:
    content = build_content_stream()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode(
            "ascii"
        )
    )
    return bytes(pdf)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(build_pdf())
    print(f"Wrote synthetic invoice PDF to {OUT}")


if __name__ == "__main__":
    main()
