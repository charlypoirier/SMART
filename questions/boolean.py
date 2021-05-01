"""
Boolean questions
1) Make a sentence positive/negative
2) Replace adjectives with their synonym/antonym
3) Replace pronouns with corresponding nouns
"""

import random
import spacy
from classes.question import Question
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

def negate_present_auxiliary(sentence):
    document = nlp(sentence)
    sentence = ""
    for token in document:
        if (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.pos_ == "AUX":
            sentence += token.text_with_ws + "not "
        else:
            sentence += token.text_with_ws
    return sentence

def negate_present_verb(sentence):
    document = nlp(sentence)
    sentence = ""
    for token in document:
        if token.pos_ == "VERB":
            if token.tag_ == "VBZ":
                sentence += "doesn't " + token.lemma_ + token.whitespace_
            elif token.tag_ == "VBP":
                sentence += "don't " + token.lemma_ + token.whitespace_
            else:
                sentence += token.text_with_ws
        else:
            sentence += token.text_with_ws
    return sentence

def generate(text):
    """
    Generate and return a set of boolean questions.
    TODO: negate() should always negate, or tell when it didn't
    TODO: fix "is not" => "is not not"
    """
    document  = nlp(text)
    sentences = document.sents
    questions = set()

    for sentence in sentences:

        n = random.randint(0, 3)
        if n == 0:
            sentence = replace_adjectives_with_synonyms(sentence.text)
            answer = True
        elif n == 1:
            sentence = replace_adjectives_with_antonyms(sentence.text)
            answer = False
        elif n == 2:
            sentence = negate_present_auxiliary(sentence.text)
            answer = False
        else:
            sentence = negate_present_verb(sentence.text)
            answer = False

        question = Question(sentence, ["True", "False"], int(not answer))
        questions.add(question)

    return questions
