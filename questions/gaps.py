#!/usr/bin/python3
import sys
import os
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

def main():
    if (len(sys.argv) !=2):
        print('Usage: python3 app.py gaps_input.txt ')
        exit(1)
    filename = sys.argv[1]
    text = ""
    with open(filename, 'r') as file:
        text = file.read()
        print(text)
    # Call a module?
    nbwords = int(len(text.split())*0.06)



    #doc = nlp(text)
    #for token in doc:
    #    print(token.text, " ",token.tag_, " : ", spacy.explain(token.tag_))
    #for ent in doc.ents:
    #    print(ent.text, " -- " ,ent.label_ ," -- ", spacy.explain(ent.label_))

    origin_nbwords = nbwords
    end = False
    while not end:
        n_keywords = keywords(text, nbwords)
        nb_diff_words = 0
        for word in n_keywords:
            #print(word)
            word_sg = wnl.lemmatize(word) #Mots au singulier
            if word != word_sg:
                if word_sg not in n_keywords:
                    nb_diff_words += 1
            else:
                nb_diff_words += 1

        print("nb-diff_words", nb_diff_words, nbwords)
        if (origin_nbwords - nb_diff_words > 0):
            nbwords += (origin_nbwords - nb_diff_words)
        else:
            end = True
        print("\nKeywords of article", n_keywords, '\n')


    bert_sentences(text, n_keywords)

    for word in n_keywords:
        #find_distractors(word)
        text = text.replace(word, '___')
        text = text.replace(word.capitalize(), '___')
        text = text.replace('___s', '___')

    print(text)


main()
