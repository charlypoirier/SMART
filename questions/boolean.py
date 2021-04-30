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

def negate_present_aux_in_a_sentence(sentence_nlp_to_negate):
    new_sentence = ""
    for token in sentence_nlp_to_negate:
        if (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.pos_ == "AUX":
            new_sentence += token.text_with_ws + "not "
        else:
            new_sentence += token.text_with_ws
    return new_sentence

def negate_present_verb_in_a_sentence(sentence_nlp_to_negate):
    new_sentence = ""
    for token in sentence_nlp_to_negate:
        if token.pos_ == "VERB":
            if token.tag_ == "VBZ":
                new_sentence += "doesn't " + token.lemma_ + token.whitespace_
            elif token.tag_ == "VBP":
                new_sentence += "don't" + token.lemma_ + token.whitespace_
            else:
                new_sentence += token.text_with_ws
        else:
            new_sentence += token.text_with_ws
    return new_sentence

def generate(text):
    """
    Generate and return a set of
    boolean questions.
    """
    document  = nlp(text)
    sentences = document.sents
    questions = set()

    for sentence in sentences:
        if bool(random.getrandbits(1)):
            sentence = replace_adjectives_with_synonyms(sentence.text)
            answer = True
        else:
            sentence = replace_adjectives_with_antonyms(sentence.text)
            answer = False
        question = Question(sentence, ["True", "False"], int(not answer))
        questions.add(question)

    return questions
