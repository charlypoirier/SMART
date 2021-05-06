#!/usr/bin/python3

"""
Interrogat"IF
Automatic quiz generation for teachers and students.

Hexanôme 4244
- Aziz Kanoun
- Charly Poirier
- Jérôme Hue
- Lucie Clémenceau
- Quentin Regaud
- Sylvain de Joannis de Verclos
"""

# Disable info and warnings
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

# Main function
def main():

    print("---------------------------------------")
    print("             INTERROGAT'IF             ")
    print("---------------------------------------")

    while True:
        print("Enter the path to your text file.")

        filepath = input("> ")
        if not os.path.isfile(filepath):
            print("Cannot find", filepath)
        else:
            break
    
    with open(filepath, "r") as file:
        text = file.read()

    print()
    print("What type of questions would you like?")
    print("1. Fill-in-the-gaps")
    print("2. True or false")
    print("3. Five Ws questions")

    while True:
        choice = input("> ")
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid choice. Please input a number.")
        
        if choice < 1 or choice > 3:
            print("Invalid choice. Please choose 1, 2 or 3.")
        else: break
    print()
    
    # Generate questions
    print("Loading components...")
    questionnaire = set()

    if choice == 1:
        from questions import spacy_keyword, gapfilling 
        print("Generating questions...")
        questionnaire = set.union(questionnaire, spacy_keyword.generate(text))
        # questionnaire = set.union(questionnaire, gapfilling.generate(text))
    elif choice == 2:
        from questions import trueorfalse
        print("Generating questions...")
        questionnaire = set.union(questionnaire, trueorfalse.generate(text))
    elif choice == 3:
        from questions import fivews
        print("Generating questions...")
        questionnaire = set.union(questionnaire, fivews.generate_wh(text))

    # Save to a file in Aikan format
    print("Saving...")
    with open("questionnaire.txt", "w") as file:
        for question in questionnaire:
            file.write(question.to_aiken())
    print("\nSaved to questionnaire.txt")


if __name__ == "__main__":
    main()
