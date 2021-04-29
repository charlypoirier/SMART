import spacy
from negspacy.negation import Negex


def main():
    nlp = spacy.load("en_core_web_sm")
    negex = Negex(nlp, ent_types=["PERSON", "ORG"])
    nlp.add_pipe("negex", config={"ent_types": ["PERSON", "ORG"]})
    doc = nlp("She does not like Steve Jobs but likes Apple products.")
    for e in doc.ents:
        print(e.text, e._.negex)