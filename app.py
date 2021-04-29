#!/usr/bin/python3
import sys
import questions.boolean

def main():
    # Parse arguments
    if (len(sys.argv) != 2):
        print('Usage: python3 app.py input.txt')
        exit(1)
    filename = sys.argv[1]
    
    # Extract the text
    text = ""
    with open(filename, 'r') as file:
        text = file.read()
    
    # Generate questions
    questionnaire = set()
    questionnaire = set.union(questionnaire, questions.boolean.generate(text))
    
    # Save to a file in Aikan format
    with open('questionnaire.txt', 'w') as file:
        for question in questionnaire:
            file.write(question.toAiken())

if __name__ == "__main__":
    main()