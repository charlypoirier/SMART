#!/usr/bin/python3

"""
Interrogat'IF
Automatic quiz generation for teachers and students.

Hexanôme 4244
- Aziz Kanoun
- Charly Poirier
- Jérôme Hue
- Lucie Clémenceau
- Quentin Regaud
- Sylvain de Joannis de Verclos
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
from questions import gaps, spacy_keyword
from questions import boolean
from questions import wh
import sys

# Main function
def main():

    if (len(sys.argv) != 2):
        print('Usage: python3 app.py input.txt')
        exit(1)
    filename = sys.argv[1]
    
    with open(filename, 'r') as file:
        text = file.read()
        text = text[:1000000]
    
    # Generate questions
    questionnaire = set()
    # questionnaire = set.union(questionnaire, wh.generate(text))
    # questionnaire = set.union(questionnaire, gaps.generate(text))
    questionnaire = set.union(questionnaire, boolean.generate(text))
    # questionnaire = set.union(questionnaire, spacy_keyword.generate(text))
    
    # Save to a file in Aikan format
    with open('questionnaire.txt', 'w') as file:
        for question in questionnaire:
            file.write(question.to_aiken())

if __name__ == '__main__':
    main()
