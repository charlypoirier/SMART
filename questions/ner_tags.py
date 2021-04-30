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

nlp = spacy.load('en_core_web_trf')

#Analyse text
doc = nlp(text)

keywords = []
distractors = {}
# Display entities and build keywords list
for ent in doc.ents:
    print(ent.text, " -- " ,ent.label_ ," -- ", spacy.explain(ent.label_))
    keywords.append(ent.text)
    #if (ent.label_ == "CARDINAL"):
    #    keywords.append(ent.text)
    #    distractors[ent.text] = [1,2,3]
    #if (ent.label_ == "ORDINAL"):
    #    keywords.append(ent.text)
    #    distractors[ent.text] = ["first", "second", "third"]

print(keywords)
print(distractors)
print('\n')

for word in keywords:
        #rp = (str(distractors[word]))
        text = text.replace(word, '__')

print(text)
