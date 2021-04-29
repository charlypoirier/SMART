import random
import spacy
from questions.Question import Question
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

"""
Boolean questions
1) Negate the sentence
2) Replace an adjective with its synonym or antonym (https://pypi.org/project/spacy-wordnet/)
3) Replace pronouns with subject from last sentence
4) Extract subject-verb-complement
"""

# Global variables
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe(WordnetAnnotator(nlp.lang))


def change_adjective(sentence):
    document = nlp(sentence)
    for token in document:
        if token.pos_ in ["ADJ"]:
            synonyms = random.choice(token._.wordnet.synsets())
            synonym = random.choice(synonyms.lemma_names())
            sentence = sentence.replace(token.text, synonym)
            print("(" + token.text + "=>" + synonym + ") ", end="")
        else:
            print(token.text + " ", end="")
    print()
    return sentence


def generate(text):

    # Split into sentences
    nlp = spacy.load("en_core_web_sm")
    document = nlp(text)
    sentences = document.sents

    # Generate questions
    questions = set()
    for sentence in sentences:
        # Replace adjectives with their synonyms
        new_sentence = change_adjective(sentence.text)
        # Create the question
        question = Question(new_sentence, "True", ["False"])
        questions.add(question)

    return questions
