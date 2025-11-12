import re

def preprocess(text):
    text = text.strip()

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Normalize currency
    text = text.replace("Rs.", "Rs ").replace("INR", "Rs")

    # Extract amount
    amount = re.findall(r'Rs\s?[\.,]?\s?(\d+)', text)
    amount = amount[0] if amount else None

    # Extract date
    date = re.findall(r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text)
    date = date[0] if date else None

    # Extract registration number
    reg = re.findall(r'(?:Reg\.? No\.?|Registration No\.?)\s?[:\-]?\s?([A-Za-z0-9]+)', text)
    reg = reg[0] if reg else None

    # Extract transaction ID
    txn = re.findall(r'(?:transaction no|txn id|transaction id)\s?[:\-]?\s?([A-Za-z0-9]+)', text, flags=re.I)
    txn = txn[0] if txn else None

    return {
        "clean_text": text,
        "amount_regex": amount,
        "date_regex": date,
        "reg_no_regex": reg,
        "transaction_regex": txn
    }
