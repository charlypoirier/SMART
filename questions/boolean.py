"""
Boolean questions
1) Negate the sentence
2) Replace an adjective with its synonym or antonym (https://pypi.org/project/spacy-wordnet/)
3) Replace pronouns with subject from last sentence
4) Extract subject-verb-complement
"""

import random
import spacy
from questions.Question import Question
from PyDictionary import PyDictionary
dictionary=PyDictionary()

# Global variables
nlp = spacy.load('en_core_web_sm')

def replace_adjectives_with_synonyms(sentence):
    document = nlp(sentence)
    for token in document:
        if token.pos_ == "ADJ":
            synonym = random.choice(dictionary.synonym(token.text))
            sentence = sentence.replace(token.text, synonym)
    return sentence
    
def replace_adjectives_with_antonyms(sentence):
    document = nlp(sentence)
    for token in document:
        if token.pos_ == "ADJ":
            synonym = random.choice(dictionary.synonym(token.text))
            sentence = sentence.replace(token.text, synonym)
    return sentence

def generate(text):
    nlp = spacy.load("en_core_web_sm")
    document = nlp(text)
    sentences = document.sents
    questions = set()
    for sentence in sentences:
        # Replace adjectives with their synonyms
        new_sentence = replace_adjectives_with_synonyms(sentence.text)
        # Add the question to the set
        question = Question(new_sentence, "True", ["False"])
        questions.add(question)

    return questions