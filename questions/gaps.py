#!/usr/bin/python3
import sys
import os
from keybert import KeyBERT
import gensim
from transformers import pipeline

unmasker = pipeline('fill-mask', model='bert-base-uncased')
print(unmasker("Oxygen is the [MASK] element with atomic number 8."))

def main():
    if (len(sys.argv) != 2):
        print('Usage: python3 questions/app.py input.txt')
        exit(1)
    filename = sys.argv[1]
    text = ""
    with open(filename, 'r') as file:
        text = file.read()
        print(text)
    # Call a module?
    

    kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
    keywords = kw_extractor.extract_keywords(text, stop_words='english')
    
    #print("Keywords of article", keywords)
    
    for word in keywords:
        text = text.replace(word[0], '___')
        text = text.replace(word[0].capitalize(), '___')

     
    print(text)

main()
