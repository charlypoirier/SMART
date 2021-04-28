#!/usr/bin/python3
import sys
from keybert import KeyBERT

def main():
    if (len(sys.argv) != 2):
        print('Usage: python3 app.py gaps_input.txt')
        exit(1)
    filename = sys.argv[1]
    text = ""
    with open(filename, 'r') as file:
        text = file.read()
        print(text)
    # Call a module?
    

    kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
    keywords = kw_extractor.extract_keywords(text, stop_words='english')
    print("Keywords of article", keywords)

main()
