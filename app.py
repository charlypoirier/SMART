#!/usr/bin/python3
from questions import gaps, boolean, wh
import sys

def main():

    # Parse arguments
    if (len(sys.argv) != 2):
        print('Usage: python3 app.py input.txt')
        exit(1)
    filename = sys.argv[1]
    
    # Extract the text
    with open(filename, 'r') as file:
        text = file.read()

    # Length limit
    text = text[:1000000]
    
    # Generate questions
    questionnaire = set()
    questionnaire = set.union(questionnaire, wh.generate(text))
    # questionnaire = set.union(questionnaire, gaps.generate(text))
    # questionnaire = set.union(questionnaire, boolean.generate(text))
    
    # Save to a file in Aikan format
    with open('questionnaire.txt', 'w') as file:
        for question in questionnaire:
            n = file.write(question.to_aiken())

if __name__ == '__main__':
    main()