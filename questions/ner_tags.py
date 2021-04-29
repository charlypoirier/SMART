import sys
import spacy

if (len(sys.argv) != 2):
    print('Usage: python3 app.py gaps_input.txt')
    exit(1)
filename = sys.argv[1]
text = ""
with open(filename, 'r') as file:
    text = file.read()
    print(text)
    # Call a module?

nlp = spacy.load('en_core_web_sm')

#Analyse text
doc = nlp(text)

keywords = []
# Display entities and build keywords list
for entities in doc.ents:
    print(entities.text, " -- " ,entities.label_ ," -- ", spacy.explain(entities.label_))
    keywords.append(entities.text)

print(keywords)
for word in keywords:
        text = text.replace(word, '___')

print(text)
