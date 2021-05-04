import spacy
import sys
import random
from classes.question import Question
from collections import Counter
from string import punctuation
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

filename = sys.argv[1]
nbwords = 0

#load spacy model
nlp = spacy.load("en_core_web_trf")


glove_file = './data/embeddings/glove.6B.100d.txt'
tmp_file = './data/embeddings/word2vec-glove.6B.100d.txt'

model = KeyedVectors.load_word2vec_format(tmp_file)
print("Model loaded", flush=True)

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
    result = {}
    doc = nlp(text)
    accept_ent = ['NORP', 'DATE', 'TIME', 'ORDINAL', 'CARDINAL']
    for ent in doc.ents:
        print('[',ent.label_ , '(', spacy.explain(ent.label_),") ] " , ent.text)
        if(ent.label_ in accept_ent):
            result[ent.text] = ent.label_
    return result



def replace_kwords(text, keywords):
    keywods =  sorted(keywords, key=len, reverse=True)
    text = ' ' + text
    i = 0
    for word in keywords:
        nword = ' ' + word + ' '
        text = text.replace(nword, " _" + str(i) +  "_ " )
        nword = ' ' + word + '.'
        text = text.replace(nword, " _" + str(i) +  "_." )
        nword = ' ' + word + ','
        text = text.replace(nword, " _" + str(i) +  "_,") 
        i = i+1
    text = text[1:]
    return text


def generate_distractors(keywords):
    options = []
    for k,v in keywords.items():
        print ("key = ", k, " - value = ", v) 
        option = [k]
        similar  = []
        if (v == 'ORDINAL'):
            similar = model.most_similar(positive=[str(k)], topn=3)
        elif (v == 'CARDINAL'):
            similar = model.most_similar(positive=[str(k)], topn=3)
        # elif (v == 'NORP'):
        #    similar = model.most_similar(positive=[str(k)], topn=3)
        else  :
            similar = [('test1',11), ('test2', 22)]
        for item in similar:
                option.append(str(item[0]))
        random.shuffle(option)
        print ("Options : " ,option)
        options.append(option)
    return options

"""text = load_text(filename)
# get hot words and remove keywords
nbwords = int(len(text.split())*0.06)
output = get_hotwords(text)
entities = get_entities(text)
print("text : ", text, "\nnbwords = ", nbwords , "\n keywords = ", output)
print("entities : ", entities)
keywords = {}

#for i in range (len(output)):
#    if (output[i] in get_entities(text)):
#        keywords.append(output[i])

keywords = entities
if len(keywords) > nbwords:
    keywords = random.sample(keywords, nbwords)

#if len(keywords) < nbwords:
#    keywords = keywords  + random.sample(output,nbwords - len(keywords))


print(keywords)
generate_distractors(keywords)
replace_kwords(text, keywords)
"""

def generate(text):
    
    nbwords = int(len(text.split())*0.06)
    output = get_hotwords(text)
    entities = get_entities(text)
    print("text : ", text, "\nnbwords = ", nbwords , "\n keywords = ", output)
    print("entities : ", entities)
    keywords = entities
   
    nkeywords = {}
    if len(keywords) > nbwords:
        i  = 0
        for k,v in keywords.items():
            nkeywords[k] = v
            i = i+1
            if (i > nbwords):
                break

    keywords = nkeywords
    #if len(keywords) > nbwords:
    #    keywords = random.sample(sorted(keywords), nbwords)

    print("Keywords : ", keywords)
    gap_text = replace_kwords(text, keywords)
    options = generate_distractors(keywords)

    #Création de la liste de questions
    questions_list_Aik = []
   
    for i in range(len(options)):
        print("Generating question :", str(i))
        gap_text_n = gap_text + "\nAnswer gap n°" + str(i) 
        q = Question(gap_text_n, options[i], 0)
        questions_list_Aik.append(q)


    return questions_list_Aik
