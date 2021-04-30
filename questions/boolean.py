"""
Boolean questions
1) Make a sentence positive/negative
2) Replace adjectives with their synonym/antonym
3) Replace pronouns with corresponding nouns
"""

import random
import spacy
from questions.Question import Question
from PyDictionary import PyDictionary

# Global variables
nlp = spacy.load('en_core_web_sm')
dictionary = PyDictionary()

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
            antonym = random.choice(dictionary.antonym(token.text))
            sentence = sentence.replace(token.text, antonym)
    return sentence

def generate(text):
    nlp = spacy.load("en_core_web_sm")
    document = nlp(text)
    sentences = document.sents
    questions = set()
    for sentence in sentences:
        sentence = replace_adjectives_with_synonyms(sentence.text)
        question = Question(sentence, "True", ["False"])
        questions.add(question)
    return questions