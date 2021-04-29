#!/usr/bin/python3
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline


unmasker = pipeline('fill-mask', model='bert-base-uncased')
print(unmasker("Oxygen is the [MASK] element with atomic number 8."))


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

    n_keywords = keywords(text, nbwords)

    print("Keywords of article", n_keywords)

    for word in n_keywords:
        text = text.replace(word, '___')
        text = text.replace(word.capitalize(), '___')

    print(text)


main()
