#!/usr/bin/python3
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
#from pattern.text.en import singularize
from nltk.stem import WordNetLemmatizer
import nltk


unmasker = pipeline('fill-mask', model='bert-base-uncased')
print(unmasker("Oxygen is the [MASK] element with atomic number 8."))
print("\n\n")

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


def main():
    if (len(sys.argv) != 3):
        print('Usage: python3 app.py gaps_input.txt [nbwords]')
        exit(1)
    filename = sys.argv[1]
    nbwords = int(sys.argv[2])
    text = ""
    with open(filename, 'r') as file:
        text = file.read()
        print(text)
    # Call a module?

    nltk.download('wordnet')
    wnl = WordNetLemmatizer()

    origin_nbwords = nbwords
    sg_word_to_add = []
    end = False
    while not end:
        n_keywords = keywords(text, nbwords)
        nb_diff_words = 0
        for word in n_keywords:
            print(word)
            word_sg = wnl.lemmatize(word) #Mets au singulier
            if word != word_sg:
                if word_sg not in n_keywords:
                    nb_diff_words += 1
                    sg_word_to_add.append(word_sg)
                else:
                    print("Plural word exists whithout singular")
            else:
                nb_diff_words += 1
        n_keywords = n_keywords + sg_word_to_add
        
        print("nb-diff_words", nb_diff_words, nbwords, origin_nbwords)
        if (origin_nbwords - nb_diff_words > 0):
            nbwords += (origin_nbwords - nb_diff_words)
        else:
            end = True
        print("\nKeywords of article", n_keywords,)

    
    through_text(n_keywords, text)

    """text = text.replace(word, '___')
    text = text.replace(word.capitalize(), '___')
    text = text.replace('___s', '___')"""

    print(text)

def through_text(n_keywords, text):
    text_words_list = text.split(" ")
    i = 0
    tab_answers =[]
    new_text_words_list = []
    for word in text_words_list:
        if word is n_keywords:
            tab_answers.append(word)
            new_text_words_list = text_words_list
            new_text_words_list[i] = "[MASK]"
        i+=1    



main()
