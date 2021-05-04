# Tout comprendre à spacy
import spacy
import sys


nlp = spacy.load('en_core_web_trf')
labels = nlp.get_pipe("tagger").labels
ent  = nlp.get_pipe("ner").labels


def print_non_punct(doc):
    for token in doc:
        if( not token.is_punct):
        #print("Morph : ", token.morph)
            print (token.text, '-', '[', token.pos_,']',spacy.explain(token.pos_), '-', spacy.explain(token.tag_), '-', '[', token.dep_ ,']',spacy.explain(token.dep_), ' - ', token.ent_type_)

# tous les labels
#print(ent)

# et les explications qui vont avec
#for tag in labels:
#    print(tag.ljust(12,'.') , spacy.explain(tag))

filename = sys.argv[1]
    
# Extract the text
text = ''
with open(filename, 'r') as file:
    text = file.read()
    text = text.replace('\n', ' ')


nbwords = int(len(text.split())*0.06)
print("nbwords : ", nbwords)

doc = nlp(text)

ents = doc.ents
sents = doc.sents
print(ents)



for sent in sents:
    print("[Sentence] : ", sent)
    print_non_punct(sent)
    print(flush=True)
#print(text, '\n')
#for token in doc:
#    if( not token.is_punct):
#        #print("Morph : ", token.morph)
#        print (token.text, '-', spacy.explain(token.pos_), '-', spacy.explain(token.tag_), '-', '[', token.dep_ ,']',spacy.explain(token.dep_), ' - ', token.ent_type_)
#        if(token.dep_ == "nsubj"):
#            print("is subject\n")

#print( "--- entities  ---" )
#for ent in doc.ents:
#   print(ent.text, " -- " ,ent.label_ ," -- ", spacy.explain(ent.label_))
