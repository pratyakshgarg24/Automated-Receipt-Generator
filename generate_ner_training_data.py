# generate_ner_training_data.py
import random, json, datetime, string, re, os

first_names = ["Pratyaksh","Aarav","Vihaan","Arjun","Karan","Rohan","Siddharth","Rahul","Aman","Kabir",
               "Ananya","Sania","Priya","Isha","Neha","Ritika","Pooja","Sneha","Divya","Kavya"]
last_names = ["Garg","Sharma","Verma","Kumar","Singh","Patel","Jain","Mehta","Gupta","Chopra",
              "Nair","Rao","Das","Iyer","Bose","Sen","Khan","Malik","Joshi","Kapoor"]
payment_methods = ["UPI","Netbanking","Card","Cash","Cheque","NEFT","IMPS"]
purposes = ["academic fees","tuition fee","exam fee","hostel fee","library fine","sports fee","lab fee","tuition"]
templates = [
    "Received Rs {amount} from {name} (Reg. No. {reg}) on {date} via {method} with transaction no {txn} for {purpose}.",
    "Payment of Rs.{amount} received from {name} Reg No {reg} dated {date} through {method}. Txn: {txn}. Purpose: {purpose}.",
    "We have received INR {amount} from {name} (Registration No: {reg}) ON {date} by {method}. Transaction ID {txn}. For {purpose}.",
    "{name} paid Rs {amount} for {purpose} (Reg. No: {reg}) on {date} via {method}. Transaction no.-{txn}",
    "Amt Rs {amount} received from {name} Reg.No:{reg} Date:{date} PayMode:{method} TxnID:{txn} For:{purpose}",
    "Received payment: {amount} INR from {name} ({reg}) on {date} via {method}. Ref {txn} Purpose: {purpose}"
]

def rand_reg():
    year = random.choice(["22","21","20","23","19"])
    dept = random.choice(["BCE","CSE","ECE","ME","EE","IT","CHE","CIV"])
    num = random.randint(1000,9999)
    return f"{year}{dept}{num}"

def rand_date():
    start = datetime.date(2023,1,1)
    end = datetime.date(2025,12,31)
    delta = (end - start).days
    d = start + datetime.timedelta(days=random.randint(0,delta))
    return d.strftime("%d/%m/%Y")

def rand_amount():
    return str(random.choice([500,1000,1500,2000,2500,5000,10000,15000,20000,25000,30000,45000,50000,75000,100000]))

def rand_txn():
    return ''.join(random.choices(string.ascii_uppercase+string.digits,k=random.randint(5,10)))

def make_entity_spans(text, mapping):
    entities = []
    for label, val in mapping.items():
        if val is None:
            continue
        # find first occurrence (case-sensitive)
        idx = text.find(val)
        if idx != -1:
            entities.append([idx, idx+len(val), label])
        else:
            m = re.search(re.escape(val), text, flags=re.I)
            if m:
                entities.append([m.start(), m.end(), label])
            # else skip
    return entities

def generate(n=1000):
    samples = []
    for i in range(n):
        template = random.choice(templates)
        name = random.choice(first_names) + " " + random.choice(last_names)
        reg = rand_reg()
        date = rand_date()
        amount = rand_amount()
        method = random.choice(payment_methods)
        txn = rand_txn()
        purpose = random.choice(purposes)
        text = template.format(amount=amount, name=name, reg=reg, date=date, method=method, txn=txn, purpose=purpose)
        # locate amount substring (the digits)
        m = re.search(r'\d{3,6}', text)
        amount_str = m.group(0) if m else None
        mapping = {
            "AMOUNT": amount_str,
            "STUDENT_NAME": name,
            "REG_NO": reg,
            "DATE": date,
            "PAYMENT_METHOD": method,
            "TRANSACTION_ID": txn,
            "PURPOSE": purpose
        }
        entities = make_entity_spans(text, mapping)
        samples.append({"text": text, "entities": entities})
    # ensure output directory exists
    os.makedirs("ner_model", exist_ok=True)
    with open("ner_model/training_data.json", "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)
    print(f"Generated {n} samples -> ner_model/training_data.json")

if __name__ == "__main__":
    generate(1000)
