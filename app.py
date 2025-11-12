import streamlit as st
import spacy
from preprocessing import preprocess
from invoice.invoice_generator import generate_invoice_html, generate_invoice_pdf

nlp = spacy.load("ner_model/model-best")

st.title("University Invoice Generator (NLP + RegEx)")

text = st.text_area("Paste SMS / Email text here:")

if st.button("Generate Invoice"):
    if text.strip() == "":
        st.error("Please enter a message.")
    else:
        # Step 1: preprocess
        regex_output = preprocess(text)
        clean_text = regex_output["clean_text"]

        # Step 2: NER extraction
        doc = nlp(clean_text)
        extracted = {ent.label_: ent.text for ent in doc.ents}

        # Include missing regex fields
        for key, val in regex_output.items():
            if key.endswith("_regex") and val:
                lbl = key.replace("_regex","").upper()
                if lbl not in extracted:
                    extracted[lbl] = val

        st.subheader("Extracted Information")
        st.json(extracted)

        # Step 3: Generate HTML Invoice
        html_invoice = generate_invoice_html(extracted)

        st.subheader("Invoice Preview")
        st.markdown(html_invoice, unsafe_allow_html=True)

        # Step 4: Generate PDF
        pdf_path = generate_invoice_pdf(html_invoice)

        # Step 5: Download button
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Invoice (PDF)",
                data=f,
                file_name="invoice.pdf",
                mime="application/pdf"
            )
