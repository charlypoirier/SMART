#!/usr/bin/python3
from questions import gaps, boolean, wh, spacy_keyword
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

    print ("********************")
    print ("")
    print ("WELCOME TO INTERROGAT'IF")
    print ("")
    print ("********************")

    print ("Select what type of questions you want to generate :")
    print ("1. True/False Questions")
    print ("2. Gap Filling Questions")
    print ("3. Wh- Question")
    print ("")

    choix = input()

    mauvais_format = True
    while (mauvais_format):
        choix = input()
        if (not choix.isnumeric() or 
           (    choix.isnumeric() and (int(choix) <1 or int(choix) >3)) ):
            print("Veuillez sélectionner un chiffre entre 1 et 3.")
        else: 
            mauvais_format = False
    print ("Le choix est : ", choix)


    
    
    # Generate questions
    questionnaire = set()

    if choix == 1:
        questionnaire = set.union(questionnaire, boolean.generate(text))
    elif choix == 2:
        questionnaire = set.union(questionnaire, spacy_keyword.generate(text))
    elif choix == 3:
        questionnaire = set.union(questionnaire, wh.generate(text))
    # questionnaire = set.union(questionnaire, gaps.generate(text))

    
    # Save to a file in Aikan format
    with open('questionnaire.txt', 'w') as file:
        for question in questionnaire:
            n = file.write(question.to_aiken())

if __name__ == '__main__':
    main()
