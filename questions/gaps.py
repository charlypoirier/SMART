#!/usr/bin/python3
import sys
import os
from classes.question import Question
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
#from pattern.text.en import singularize
from nltk.stem import WordNetLemmatizer
import nltk
import spacy
import gensim
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors


glove_file = '../data/embeddings/glove.6B.300d.txt'
tmp_file = '../data/embeddings/word2vec-glove.6B.300d.txt'

nltk.download('wordnet')
wnl = WordNetLemmatizer()
unmasker = pipeline('fill-mask', model='bert-base-uncased')

print("--------------------------\n")

if not os.path.isfile(glove_file):
    print("Glove embeddings not found. Please download and place them in the following path: " + glove_file)

def keywords(text, top_n):
    n_gram_range = (1, 1)
    stop_words = "english"

    # Extract candidate words/phrases
    count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([text])
    candidates = count.get_feature_names()
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    doc_embedding = model.encode([text])
    candidate_embeddings = model.encode(candidates)
    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    top_n_keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]

    return top_n_keywords

# Renvoie la liste complète des mots clés du texte
# Utilise la fonction keywords(text, top_n) puis rajoute au tableau des mots clés 
# les singuliers, des majuscules aux premiers mots
def formated_keywords(text):
    #nbwords = int(len(text.split())*0.06)
    nbwords = 4

    origin_nbwords = nbwords
    sg_words_to_add = []
    end = False
    while not end:
        n_keywords = keywords(text, nbwords)
        nb_diff_words = 0
        sg_words_to_add = []
        for word in n_keywords:
            #print(word)
            word_sg = wnl.lemmatize(word) #Mots au singulier
            if word != word_sg:
                if word_sg not in n_keywords:
                    nb_diff_words += 1
                    sg_words_to_add.append(word_sg)
            else:
                nb_diff_words += 1
        for word_to_add in sg_words_to_add:
            if word_to_add not in n_keywords:
                n_keywords.append(word_to_add)
        #print("nb-diff_words", nb_diff_words, nbwords, origin_nbwords)
        if (origin_nbwords - nb_diff_words > 0):
            nbwords += (origin_nbwords - nb_diff_words)
        else:
            end = True

        words_C = []
        for word in n_keywords:
            words_C.append(word.capitalize())
        n_keywords = n_keywords + words_C

        print("\nKeywords of article", n_keywords, '\n')
    return n_keywords


def find_distractors(word):
    #from gensim.scripts.glove2word2vec import glove2word2vec
    #glove2word2vec(glove_file, tmp_file)
    model = KeyedVectors.load_word2vec_format(tmp_file)
    print("distractors for ", word)
    print(model.most_similar(positive=[word], topn=3))



def bert_sentences(text, keywords):
    nlp = spacy.load('en_core_web_sm')
    mask = "[MASK]"
    for word in keywords:
        text = text.replace(word, mask)
        text = text.replace(word.capitalize(), mask)
        text = text.replace('[MASK]s', mask)
        print("keyword :", word)
    doc = nlp(text)
    for sent in doc.sents:
        sentence = str(sent)
        if(sentence.count("[MASK]") == 1):
            print(sentence)
            usent = unmasker(sentence)
            #print(truc["token_str"])
            #print(truc)
            for item in usent:
                print(item["token_str"])
            print("\n\n")

# Fonction qui parcourt le texte pour trouver les mots clés à cacher.
# Pour chaque mot clé, on stocke le mot caché et on trouve els distracteurs
# La fonction renvoie 
# - la liste des mots cachés, 
# - la liste des distracteurs de chaque mot caché (lise de liste)
# - le texte avec les trous _i_
def through_text(text):
    nlp = spacy.load('en_core_web_sm')
    text_tokens_list = nlp(text)#On récupère chaque mot du texte et ses informations
    text_words_list =[]

    #On convertit la liste de tokens en une liste de mots
    for token in text_tokens_list:
        text_words_list.append(token.text)
    print ("TT")

    i = 0
    tab_answers =[]#Stocke les mots originaux
    mask_text_words_list = []# Stocke tous les mots du text avec un qui est remplacé par [MASK]
    mask_text = []#Nouveau texte avec [MASK]
    distractors = []
    gap_text_list = []#liste de mots formant le texte avec les gaps _i_
    n_keywords = formated_keywords(text)
    for word in text_words_list:
        if word in n_keywords:
            gap = "_"+str(i)+"_"
            gap_text_list.append(gap)
            tab_answers.append(word)
            mask_text_words_list = []
            mask_text_words_list = text_words_list [:]
            mask_text_words_list[i] = "[MASK]"
            mask_text = " ".join(mask_text_words_list)
            #distractors.append( FIND DISTRACTORS )
            distractors.append(unmasker(mask_text ))
            i+=1        
        else:
            gap_text_list.append(word)
    #Refactorisation du texte
    gap_text = " ".join(gap_text_list)
    gap_text = gap_text.replace(" ,", ",")
    gap_text = gap_text.replace(" .", ".")
    gap_text = gap_text.replace(" 's", "'s")
    gap_text = gap_text.replace(" )", ")")
    gap_text = gap_text.replace("( ", "(")
    return [tab_answers, distractors, gap_text]

def generate(text):
    #On crée les réponses, les distracteurs et le texte avec les trous
    [tab_answers, distractors, gap_text] = through_text(text)

    """Debug
    print ("\n\n**********Gap Text************ ", "\n\n") 
    print(gap_text)

    print ("\n\n**********Réponses************ ", "\n\n") 
    
    print (text)
    """

    #Création de la liste de questions
    i=0
    questions_list_Aik = []
    for groupe in distractors:
        print (i, tab_answers[i])
        options = []
        options.append(tab_answers[i])
        for prop in groupe:
            option = prop["token_str"]
            options.append(option)
            print (option)
        gap_text_n = gap_text + "\nAnswer gap n°" + str(i)
        q = Question(gap_text_n, options, 0)
        questions_list_Aik.append(q)
        questions_list_Aik.append(q)
        print("\n\n")
        i += 1

    return questions_list_Aik

#generate()
