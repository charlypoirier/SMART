import spacy
import sys
import random
from collections import Counter
from string import punctuation

filename = sys.argv[1]
nbwords = 0

#load spacy model
nlp = spacy.load("en_core_web_md")



# load text function
def load_text(filename):
    with open(filename, 'r') as file:
        text = file.read()
    text = text.replace('\n', ' ')
    return text


#hotword function
def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'NUM'] # 1
    doc = nlp(text) # 2
    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)

    return result # 5

def get_entities(text):
    result =[]
    doc = nlp(text)
    for ent in doc.ents:
        result.append(ent.text)
    return result



def replace_kwords(text, keywords):
    for word in keywords:
        nword = ' ' + word + ' '
        text = text.replace(nword, " ___ ")
    print(text)




text = load_text(filename)
# get hot words and remove keywords
nbwords = int(len(text.split())*0.06)
output = get_hotwords(text)
print("text : ", text, "\nnbwords = ", nbwords , "\n keywords = ", output)
print("entities : ", get_entities(text))
keywords = [] 




#for i in range (len(output)):
#    if (output[i] in get_entities(text)):
#        keywords.append(output[i])

keywords = keywords + get_entities(text)
if len(keywords) > nbwords:
    keywords = random.sample(keywords, len(keywords) - nbwords)

if len(keywords) < nbwords:
    keywords = keywords  + random.sample(output,nbwords - len(keywords))


print(keywords)

replace_kwords(text, keywords)
