import spacy
from spacy.training.example import Example
import json

def train_model():
    nlp = spacy.blank("en")

    ner = nlp.add_pipe("ner")

    labels = ["STUDENT_NAME", "REG_NO", "AMOUNT", "DATE", "PAYMENT_METHOD", "TRANSACTION_ID", "PURPOSE"]
    for label in labels:
        ner.add_label(label)

    with open("training_data.json", "r") as f:
        TRAIN_DATA = json.load(f)

    optimizer = nlp.begin_training()

    for epoch in range(50):
        losses = {}
        for data in TRAIN_DATA:
            text = data["text"]
            entities = data["entities"]
            example = Example.from_dict(nlp.make_doc(text), {"entities": entities})
            nlp.update([example], drop=0.3, losses=losses)

        print(f"Epoch {epoch}: {losses}")

    nlp.to_disk("model-best")

if __name__ == "__main__":
    train_model()
