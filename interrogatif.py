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

print("Importing modules...")
from questions import spacy_keyword, gapfilling 
from questions import trueorfalse
from questions import fivews

# Clear the console
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# Main function
def main():
    while True:
        clear()
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃            INTERROGAT'IF            ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

        while True:
            print("Enter the path to your text file.")

            filepath = input("> ")
            if not os.path.isfile(filepath):
                print("Cannot find", filepath, "\n")
            else:
                break
        
        input_file = open(filepath, "r")
        text = input_file.read()
        input_file.close()

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
        print("Generating questions...")
        questionnaire = set()
        if choice == 1:
            questionnaire = set.union(questionnaire, spacy_keyword.generate(text))
            # questionnaire = set.union(questionnaire, gapfilling.generate(text))
        elif choice == 2:
            questionnaire = set.union(questionnaire, trueorfalse.generate(text))
        elif choice == 3:
            questionnaire = set.union(questionnaire, fivews.generate_wh(text))

        # Save to a file in Aikan format
        output_file = open(filepath+".aiken", "w")
        for question in questionnaire:
            output_file.write(question.to_aiken())
        output_file.close()
        print("Saved to "+filepath+".aiken\n")

        input("Press enter to continue.")


if __name__ == "__main__":
    main()
