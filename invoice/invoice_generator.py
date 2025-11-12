import os
import pdfkit
from jinja2 import Template

def generate_invoice_html(data):
    # template path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "templates", "invoice_template.html")

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    html = template.render(
        name=data.get("STUDENT_NAME", "N/A"),
        reg=data.get("REG_NO", "N/A"),
        amount=data.get("AMOUNT", "N/A"),
        date=data.get("DATE", "N/A"),
        method=data.get("PAYMENT_METHOD", "N/A"),
        txn=data.get("TRANSACTION_ID", "N/A"),
        purpose=data.get("PURPOSE", "N/A")
    )
    return html


def generate_invoice_pdf(html):
    pdf_path = "generated_invoice.pdf"
    pdfkit.from_string(html, pdf_path)
    return pdf_path
