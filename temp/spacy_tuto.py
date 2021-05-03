# Tout comprendre à spacy
import spacy

nlp = spacy.load('en_core_web_trf')
labels = nlp.get_pipe("tagger").labels
ent  = nlp.get_pipe("ner").labels

# tous les labels
print(ent)

# et les explications qui vont avec
for tag in labels:
    print(tag.ljust(12,'.') , spacy.explain(tag))
