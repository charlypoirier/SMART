#!/usr/bin/python3
import sys
from keybert import KeyBERT

def main():
    if (len(sys.argv) != 2):
        print('Usage: python3 app.py input.txt')
        exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        text = file.read()
        print(text)
    # Call a module?
    
    text = "The quick brown fox jumps over the lazy dog."

    kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
    for j in range(len(array_text)):
        keywords = kw_extractor.extract_keywords(text, stop_words='english')
    print("Keywords of article", keywords)
    

# Guard preventing this script to be run more
# than once when being imported from other scripts
if __name__ == "__main__":
    main()
