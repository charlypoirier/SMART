# Tout comprendre à spacy
import spacy

nlp = spacy.load('en_core_web_trf')
labels = nlp.get_pipe("tagger").labels

# tous les labels
print(labels)

# et les explications qui vont avec
for tag in labels:
    print(tag.ljust(12,'.') , spacy.explain(tag))
