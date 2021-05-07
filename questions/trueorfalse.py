import random
import spacy
from classes.question import Question
from re import search
from libs.language import *


def generate(text):
    """
    Generate and return a set of boolean questions.
    """
    text = replace_which_he_she_words(text)
    sentences = nlp(text).sents
    sentences = extract_clauses(sentences)
    questions = set()

    for sentence in sentences:
        n = random.randint(0, 4)

        while n == 2 and not is_negation_accepted(nlp(sentence)):
            n = random.randint(0, 1)
        if n == 0:
            [sentence, replaced] = replace_adjectives_with_synonyms(sentence)
            answer = replaced
        elif n == 1:
            [sentence, replaced] = replace_adjectives_with_antonyms(sentence)
            answer = not replaced
        else:
            [sentence, negated] = negate_present_or_past_sentence(nlp(sentence))
            answer = not negated
        sentence = sentence.strip() + "."

        question = Question(sentence, ["True", "False"], int(not answer))
        questions.add(question)

    return questions










def replace_adjectives_with_synonyms(sentence):
    document = nlp(sentence)
    replaced = False
    for token in document:
        if token.pos_ == "ADJ":
            synonyms = dictionary.synonym(token.text)
            if synonyms is not None:
                replaced = True
                synonym = random.choice(synonyms)
                sentence = sentence.replace(token.text, synonym)
                break
    return [sentence, replaced]


def replace_adjectives_with_antonyms(sentence):
    document = nlp(sentence)
    replaced = False
    for token in document:
        if token.pos_ == "ADJ":
            antonyms = dictionary.antonym(token.text)
            if antonyms is not None:
                replaced = True
                antonym = random.choice(antonyms)
                sentence = sentence.replace(token.text, antonym)
                break
    return [sentence, replaced]


# test if there is already a negative formed verb  in the sentence
def is_negation_accepted(sentence_nlp_to_test):
    contain_verb = False
    for token in sentence_nlp_to_test:
        if token.dep_ == "neg" and token.tag_ == "RB":  # is it a negative word
            return False
        elif token.tag_ == "VBZ" or token.tag_ == "VBP" or token.tag_ == "VBD":
            contain_verb = True
    return contain_verb


def negate_present_or_past_sentence(sentence_nlp_to_negate):
    new_sentence = ""
    negated = False
    for token in sentence_nlp_to_negate:
        if hasattr(token, "pos_"):
            if token.pos_ == "AUX":
                # 3rd person singular present or  non-3rd person singular present or past tense
                if token.tag_ == "VBZ" or token.tag_ == "VBP" or token.tag_ == "VBD":
                    negated = False
                    new_sentence += token.text + token.whitespace_ + "not" + token.whitespace_
                else:
                    new_sentence += token.text_with_ws
            elif token.pos_ == "VERB":
                if token.tag_ == "VBZ":  # 3rd person singular present
                    negated = True
                    new_sentence += "doesn't" + token.whitespace_ + token.lemma_ + token.whitespace_
                elif token.tag_ == "VBP":  # non-3rd person singular present
                    negated = True
                    new_sentence += "don't" + token.whitespace_ + token.lemma_ + token.whitespace_
                elif token.tag_ == "VBD":  # verb, past tens
                    negated = True
                    new_sentence += "didn't" + token.whitespace_ + token.lemma_ + token.whitespace_
                else:
                    new_sentence += token.text_with_ws
            else:
                new_sentence += token.text_with_ws
        else:
            if hasattr(token, 'text_with_ws'):
                new_sentence += token.text_with_ws
    return [new_sentence, negated]


def get_chunk_from_word(sentence_nlp, word):
    for c in sentence_nlp.noun_chunks:
        if search(word, c.text):
            return c.text
    return "not found"


def replace_which_he_she_words(text):
    doc = nlp(text)
    sentences = doc.sents
    new_text = ""
    last_person_subject = "undefined"
    for sentence_nlp in sentences:
        last_subject = "undefined"
        for token in sentence_nlp:
            #      token.dep_ + " ; head: " + token.head.text + " ;right-edge: " + token.right_edge.text + " ; sent : "
            #      , token.ent_iob)
            if (token.tag_ == "NNP" or token.tag_ == "NN") and token.dep_ == "nsubj":
                last_person_subject = token.text

            if token.tag_ == "PRP" and token.dep_ == "nsubj" and last_person_subject != "undefined":  # case : "he" or "she"
                c = get_chunk_from_word(doc, last_person_subject)
                if c != "not found" and (token.text == "he"
                                         or token.text == "she"
                                         or token.text == "She"
                                         or token.text == "He"):
                    new_text += " " + c
                else:
                    new_text += " " + token.text
            elif token.dep_ == "pobj":
                last_subject = token.text
                new_text += " " + token.text
            elif token.tag_ == "WDT" and not token.i == 0: # case : which
                if last_subject != "undefined":
                    c = get_chunk_from_word(sentence_nlp, last_subject)
                    if c != "not found":
                        new_text += ". " + c.capitalize()
                    else:
                        new_text += " " + token.text
                else:
                    new_text += " " + token.text
            else:
                new_text += " " + token.text
    return new_text

