import spacy
import sys
import random
from classes.question import Question
from collections import Counter
from string import punctuation
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import re
from libs.language import *

# TODO: Mettre ça dans gaps.py ?

# voir https://github.com/KristiyanVachev/Question-Generation 
glove_file = './data/embeddings/glove.6B.100d.txt'
tmp_file = './data/embeddings/word2vec-glove.6B.100d.txt'

model = KeyedVectors.load_word2vec_format(tmp_file)


def generate(text):
    nbwords = int(len(text.split())*0.06)
    output = get_hotwords(text)
    entities = get_entities(text)
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

    gap_text = replace_kwords(text, keywords)
    [options, answers] = generate_distractors(keywords)

    #Création de la liste de questions
    questions_list_Aik = []
   
    for i in range(len(options)):
        gap_text_n = gap_text + "\nAnswer gap n°" + str(i) 
        q = Question(gap_text_n, options[i], answers[i])
        questions_list_Aik.append(q)

    return questions_list_Aik


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
        if(ent.label_ in accept_ent):
            result[ent.text] = ent.label_
    return result


def replace_kwords(text, keywords):
    keywods =  sorted(keywords, key=len, reverse=True)
    text = ' ' + text
    i = 0
    for word in keywords:
        nword = ' ' + word + ' '
        text = text.replace(nword, " _" + str(i) +  "_ ", 1)
        nword = ' ' + word + '.'
        text = text.replace(nword, " _" + str(i) +  "_.", 1)
        nword = ' ' + word + ','
        text = text.replace(nword, " _" + str(i) +  "_,", 1) 
        nword = ' ' + word + '-'
        text = text.replace(nword, " _" + str(i) +  "_-", 1) 
        i = i+1
    text = text[1:]
    return text


def generate_distractors(keywords):
    options = []
    answers = []
    for k,v in keywords.items():
        option = [str(k)]
        similar  = []
        if (v == 'ORDINAL'):
            similar = model.most_similar(positive=[str(k)], topn=3)
        elif (v == 'CARDINAL'):
            similar = model.most_similar(positive=[str(k)], topn=3)
        elif (v == 'NORP'):
            similar = model.most_similar(positive=[str(k).lower()], topn=3)
            option = []
            t = k.lower()
            option = [t]
        elif (v == 'TIME'):
            
            regexp  = re.compile('([0-1]?[0-9]|2[0-3]):[0-5][0-9]')
            regexp2 = re.compile('([0-5][0-9]|[1-9])')
            if regexp.search(str(k)):

                stringtorep = str(k)
                
                h = random.randint(0,23)
                m = random.randint(0,59)
                repl = str(h) + ':' + str(f'{m:02d}')
                ret  = re.sub('([0-1]?[0-9]|2[0-3]):[0-5][0-9]', repl, stringtorep)
                
                h = random.randint(0,23)
                m = random.randint(0,59)
                repl = str(h) + ':' + str(f'{m:02d}')
                ret2  = re.sub('([0-1]?[0-9]|2[0-3]):[0-5][0-9]', repl, stringtorep)
            
                similar = [(ret,11), (ret2, 22)]
            elif regexp2.search(str(k)):
                stringtorep = str(k)
                
                m = random.randint(0,59)
                repl = str(m)
                ret  = re.sub('([0-5][0-9]|[1-9])', repl, stringtorep)
                m = random.randint(0,59)
                repl = str(m)
                ret2  = re.sub('([0-5][0-9]|[1-9])', repl, stringtorep)

                similar = [(ret,11), (ret2, 22)]

            else:
                similar = [('test1',11), ('test2', 22)]
        elif (v == 'DATE'):
            regexp  = re.compile('( [1-9] | [12]\d | 3[01] )')
            regexp2 = re.compile('( [1-9],| [12]\d,| 3[01],)')
            regexp3 = re.compile('([A-Za-z]*)')
            regexp4 = re.compile('[0-9]*')
            nk = ' ' + str(k) + ' '
            if regexp.search(nk):
                day = random.randint(1,31)
                ret = re.sub('( [1-9] | [12]\d | 3[01] )', ' ' +str(day) + ' ', nk)
                day = random.randint(1,31)
                ret2 = re.sub('( [1-9] | [12]\d | 3[01] )',' ' +str(day) + ' ', nk)
                similar = [(ret[1:],11), (ret2[1:], 22)]
            elif regexp2.search(nk): 
                day = random.randint(1,31)
                ret = re.sub('( [1-9],| [12]\d,| 3[01],)', ' ' +str(day) + ',', nk)
                day = random.randint(1,31)
                ret2 = re.sub('( [1-9],| [12]\d,| 3[01],)',' ' +str(day) + ',', nk)
                similar = [(ret[1:],11), (ret2[1:], 22)]
            elif ( regexp3.search(str(k)) ):
                similar = model.most_similar(positive=[str(k).lower()], topn=3)
            else :
                similar = [('date1',11), ('date2', 22)]
        else  :
            similar = [('test1',11), ('test2', 22)]
        for item in similar:
                option.append(str(item[0]))
        ans = option[0]
        random.shuffle(option)
        answers.append(option.index(ans))
        options.append(option)
    return [options, answers]

