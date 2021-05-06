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
    sentences = preprocessing(sentences)
    questions = set()

    for sentence in sentences:
        n = random.randint(0, 4)

        while n == 2 and not is_negation_accepted(nlp(sentence)):
            n = random.randint(0, 1)

        if n == 0:
            sentence = replace_adjectives_with_synonyms(sentence)
            answer = True
        elif n == 1:
            sentence = replace_adjectives_with_antonyms(sentence)
            answer = False
        else:
            sentence = negate_present_or_past_sentence(nlp(sentence))
            answer = False

        question = Question(sentence, ["True", "False"], int(not answer))
        questions.add(question)

    return questions


def cartesian_product(left, right):
    if len(left) > 0 and len(right) == 0:
        return left
    elif len(left) == 0 and len(right) > 0:
        return right
    else:
        res = []
        for elem in left:
            for elem2 in right:
                res.append(elem+elem2)
        return res


def append_token_to_list(token, comb_l, comb_r):
    if len(comb_l) > 0:
        for elem in comb_l:
            elem.append(token)
        return
    if len(comb_r) > 0:
        for elem in comb_r:
            elem.insert(0, token)
        return


def complete_verb(token):
    verb_phrase = str(token)
    left_phrase = ""
    for leftchild in token.lefts:
        if leftchild.dep_ == "auxpass" or leftchild.dep_ == "aux":
            left_phrase = left_phrase+str(leftchild)+" "
    verb_phrase = left_phrase+verb_phrase
    for rightchild in token.rights:
        if rightchild.dep_ == "dative":
            verb_phrase = verb_phrase + " "+str(rightchild)
    return verb_phrase


def tt_comb_subj(token):
    list_comb = []
    vide = []
    vide.append(' ')
    if token.n_rights == 0 and token.n_lefts == 0:
        id = []
        id.append(token)
        list_comb.append(id)
        if (token.dep_ != "amod" and token.dep_ != "mark" and token.dep_ != "det" and token.dep_ != "compound"
                and token.dep_ != "dative" and token.dep_ != "poss" and token.dep_ != "agent" and token.dep_ != "quantmod" and token.dep_ != "nummod"):  # amod et det sont obligatoires
            list_comb.append(vide)
        return list_comb
    else:
        left = []
        right = []
        for left_child in token.lefts:
            left = cartesian_product(
                left, tt_comb_obj(left_child))
        for right_child in token.rights:
            right = cartesian_product(
                right, tt_comb_obj(right_child))
        append_token_to_list(token, left, right)
        # right.append(vide)
        list_comb = cartesian_product(left, right)
        if (token.dep_ != "pobj" and token.dep_ != "mark" and token.dep_ != "prep" and token.dep_ != "nummod" and token.dep_ != "pcomp" and
                token.dep_ != "compound" and token.dep_ != "dative" and token.dep_ != "nsubjpass" and token.dep_ != "poss" and token.dep_ != "quantmod" and token.dep_ != "agent" and token.dep_ != "expl"):  # pobj et prep sont obligatoires
            list_comb.append(vide)
        return list_comb


def tt_comb_obj(token):
    list_comb = []
    vide = []
    vide.append(' ')
    if token.n_rights == 0 and token.n_lefts == 0:
        id = []
        id.append(token)
        list_comb.append(id)
        if (token.dep_ != "dobj" and token.dep_ != "mark" and token.dep_ != "amod" and token.dep_ != "det" and token.dep_ != "nsubj"
            and token.dep_ != "pobj" and token.dep_ != "compound" and token.dep_ != "dative" and token.dep_ != "poss" and token.dep_ != "pcomp" and token.dep_ != "expl"
            and token.dep_ != "cc" and token.dep_ != "conj" and token.dep_ != "advmod" and token.dep_ != "nsubjpass" and token.dep_ != "nummod" and token.dep_ != "quantmod" and token.dep_ != "nmod"
                and token.dep_ != "agent" and token.dep_ != "aux" and token.dep_ != "npadvmod" and token.dep_ != "auxpass"):  # amod et det sont obligatoires
            list_comb.append(vide)
        return list_comb
    else:
        left = []
        right = []
        for left_child in token.lefts:
            left = cartesian_product(
                left, tt_comb_obj(left_child))
        for right_child in token.rights:
            right = cartesian_product(
                right, tt_comb_obj(right_child))
        append_token_to_list(token, left, right)
        list_comb = cartesian_product(left, right)
        if (token.dep_ != "dobj" and token.dep_ != "expl" and token.dep_ != "aux" and token.dep_ != "quantmod" and token.dep_ != "mark" and token.dep_ != "pobj" and token.dep_ != "pcomp"
            and token.dep_ != "prep" and token.dep_ != "nsubj" and token.dep_ != "nsubjpass" and token.dep_ != "poss" and token.dep_ != "pobj" and token.dep_ != "conj" and token.dep_ != "dative" and token.dep_ != "agent"
                and token.dep_ != "compound" and token.dep_ != "npadvmod" and token.dep_ != "auxpass" and token.dep_ != "aux" and token.dep_ != "nmod" and token.dep_ != "attr" and token.dep_ != "nummod"):  # pobj et prep sont obligatoires
            list_comb.append(vide)
        return list_comb


def remove_whitespace(obj_list):
    if len(obj_list) > 1 and obj_list[-1] == [' ']:
        obj_list.pop()
    elif len(obj_list) == 0 and obj_list[0] == [' ']:
        obj_list.pop()


def visit_rule(token, right_child, subj_dep, obj_dep, obj_pos):
    subject_found = False
    clause = ""
    verb = complete_verb(token)
    list_subj = []
    list_obj = []
    list_clause = []
    clause_list = []
    for child in token.lefts:
        if child.dep_ in subj_dep:
            list_subj = tt_comb_subj(child)
            remove_whitespace(list_subj)
            subject_found = True
            break
    append_token_to_list(verb, list_subj, list_obj)
    if subject_found == True and right_child.pos_ in obj_pos and right_child.dep_ in obj_dep:
        list_obj = tt_comb_obj(right_child)
        remove_whitespace(list_obj)
        list_clause = cartesian_product(list_subj, list_obj)
        for phrase in list_clause:
            clause = ""
            for word in phrase:
                if str(word) != " ":
                    clause = clause + str(word) + " "
            clause_list.append(clause)
    return clause_list


def visit_verb(token):
    clause_list = []
    for child in token.rights:
        if child.dep_ == "conj":
            # (nsubj)  (verb) (conj vers NOUN)
            clause_list = clause_list + \
                visit_rule(token, child, ["nsubj"], ["conj"], ["NOUN"])
        if child.dep_ == "dobj":
            # (nsubj)  (verb) (dobj vers NOUN)
            clause_list = clause_list + \
                visit_rule(token, child, ["nsubj"], ["dobj"], ["NOUN"])
        if child.dep_ == "prep":
            # nsubjpass (VERB) prep vers ADP
            clause_list = clause_list + \
                visit_rule(token, child, ["nsubjpass"], ["prep"], ["ADP"])
            # nsubjpass (VERB) prep vers SCONJ
            clause_list = clause_list + \
                visit_rule(token, child, ["nsubjpass"], ["prep"], ["SCONJ"])
        if child.dep_ == "attr":
            # PRON<-expl|nsubj- AUX -attr->NOUN
            clause_list = clause_list + \
                visit_rule(token, child, ["expl", "nsubj"], [
                              "attr"], ["NOUN"])
    return clause_list



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
    for token in sentence_nlp_to_negate:
        if hasattr(token, "pos_"):
            if token.pos_ == "AUX":
                # 3rd person singular present or  non-3rd person singular present or past tense
                if token.tag_ == "VBZ" or token.tag_ == "VBP" or token.tag_ == "VBD":
                    new_sentence += token.text + token.whitespace_ + "not" + token.whitespace_
                else:
                    new_sentence += token.text_with_ws
            elif token.pos_ == "VERB":
                if token.tag_ == "VBZ":  # 3rd person singular present
                    new_sentence += "doesn't" + token.whitespace_ + token.lemma_ + token.whitespace_
                elif token.tag_ == "VBP":  # non-3rd person singular present
                    new_sentence += "don't" + token.whitespace_ + token.lemma_ + token.whitespace_
                elif token.tag_ == "VBD":  # verb, past tens
                    new_sentence += "didn't" + token.whitespace_ + token.lemma_ + token.whitespace_
                else:
                    new_sentence += token.text_with_ws
            else:
                new_sentence += token.text_with_ws
        else:
            if hasattr(token, 'text_with_ws'):
                new_sentence += token.text_with_ws
    return new_sentence


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

