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
from re import search

# Global variables
nlp = spacy.load('en_core_web_sm')
dictionary = PyDictionary()


def cartesian_product(combi_gauche, combi_droite):
    if len(combi_gauche) > 0 and len(combi_droite) == 0:
        return combi_gauche
    elif len(combi_gauche) == 0 and len(combi_droite) > 0:
        return combi_droite
    else:
        res = []
        for elem in combi_gauche:
            for elem2 in combi_droite:
                res.append(elem+elem2)
        return res


def appendtokenToList(token, combig, combid):
    if(len(combig) > 0):
        for elem in combig:
            elem.append(token)
        return
    if(len(combid) > 0):
        for elem in combid:
            elem.insert(0, token)
        return


def complete_Verb(token):
    verb_phrase = str(token)
    left_phrase = ""
    for leftchild in token.lefts:
        if (leftchild.dep_ == "auxpass" or leftchild.dep_ == "aux"):
            left_phrase = left_phrase+str(leftchild)+" "
    verb_phrase = left_phrase+verb_phrase
    for rightchild in token.rights:
        if (rightchild.dep_ == "dative"):
            verb_phrase = verb_phrase + " "+str(rightchild)
    return verb_phrase


def tt_combi_Subj(token):
    list_combi = []
    vide = []
    vide.append(' ')
    if (token.n_rights == 0 and token.n_lefts == 0):
        id = []
        id.append(token)
        list_combi.append(id)
        if (token.dep_ != "amod" and token.dep_ != "mark" and token.dep_ != "det" and token.dep_ != "compound"
                and token.dep_ != "dative" and token.dep_ != "poss" and token.dep_ != "agent" and token.dep_ != "quantmod" and token.dep_ != "nummod"):  # amod et det sont obligatoires
            list_combi.append(vide)
        return list_combi
    else:
        combi_gauche = []
        combi_droite = []
        for leftchild in token.lefts:
            combi_gauche = cartesian_product(
                combi_gauche, tt_combi_Obj(leftchild))
        for rightchild in token.rights:
            combi_droite = cartesian_product(
                combi_droite, tt_combi_Obj(rightchild))
        appendtokenToList(token, combi_gauche, combi_droite)
        # combi_droite.append(vide)
        list_combi = cartesian_product(combi_gauche, combi_droite)
        if (token.dep_ != "pobj" and token.dep_ != "mark" and token.dep_ != "prep" and token.dep_ != "nummod" and token.dep_ != "pcomp" and
                token.dep_ != "compound" and token.dep_ != "dative" and token.dep_ != "nsubjpass" and token.dep_ != "poss" and token.dep_ != "quantmod" and token.dep_ != "agent" and token.dep_ != "expl"):  # pobj et prep sont obligatoires
            list_combi.append(vide)
        return list_combi


def tt_combi_Obj(token):
    list_combi = []
    vide = []
    vide.append(' ')
    if (token.n_rights == 0 and token.n_lefts == 0):
        id = []
        id.append(token)
        list_combi.append(id)
        if (token.dep_ != "dobj" and token.dep_ != "mark" and token.dep_ != "amod" and token.dep_ != "det" and token.dep_ != "nsubj"
            and token.dep_ != "pobj" and token.dep_ != "compound" and token.dep_ != "dative" and token.dep_ != "poss" and token.dep_ != "pcomp" and token.dep_ != "expl"
            and token.dep_ != "cc" and token.dep_ != "conj" and token.dep_ != "advmod" and token.dep_ != "nsubjpass" and token.dep_ != "nummod" and token.dep_ != "quantmod" and token.dep_ != "nmod"
                and token.dep_ != "agent" and token.dep_ != "aux" and token.dep_ != "npadvmod" and token.dep_ != "auxpass"):  # amod et det sont obligatoires
            list_combi.append(vide)
        return list_combi
    else:
        combi_gauche = []
        combi_droite = []
        for leftchild in token.lefts:
            combi_gauche = cartesian_product(
                combi_gauche, tt_combi_Obj(leftchild))
        for rightchild in token.rights:
            combi_droite = cartesian_product(
                combi_droite, tt_combi_Obj(rightchild))
        appendtokenToList(token, combi_gauche, combi_droite)
        list_combi = cartesian_product(combi_gauche, combi_droite)
        if (token.dep_ != "dobj" and token.dep_ != "expl" and token.dep_ != "aux" and token.dep_ != "quantmod" and token.dep_ != "mark" and token.dep_ != "pobj" and token.dep_ != "pcomp"
            and token.dep_ != "prep" and token.dep_ != "nsubj" and token.dep_ != "nsubjpass" and token.dep_ != "poss" and token.dep_ != "pobj" and token.dep_ != "conj" and token.dep_ != "dative" and token.dep_ != "agent"
                and token.dep_ != "compound" and token.dep_ != "npadvmod" and token.dep_ != "auxpass" and token.dep_ != "aux" and token.dep_ != "nmod" and token.dep_ != "attr" and token.dep_ != "nummod"):  # pobj et prep sont obligatoires
            list_combi.append(vide)
        return list_combi


def remove_whitespace(objlist):
    if (len(objlist) > 1 and objlist[-1] == [' ']):
        objlist.pop()
    elif (len(objlist) == 0 and objlist[0] == [' ']):
        objlist.pop()


def visiter_regle(token, right_child, subj_dep, obj_dep, obj_pos):
    subject_found = False
    clause = ""
    verb = complete_Verb(token)
    list_subj = []
    list_obj = []
    list_clause = []
    clause_list = []
    for child in token.lefts:
        if child.dep_ in subj_dep:
            list_subj = tt_combi_Subj(child)
            remove_whitespace(list_subj)
            subject_found = True
            break
    appendtokenToList(verb, list_subj, list_obj)
    if (subject_found == True and right_child.pos_ in obj_pos and right_child.dep_ in obj_dep):
        list_obj = tt_combi_Obj(right_child)
        remove_whitespace(list_obj)
        list_clause = cartesian_product(list_subj, list_obj)
        for phrase in list_clause:
            clause = ""
            for word in phrase:
                if (str(word) != " "):
                    clause = clause+str(word)+" "
            clause_list.append(clause)
    return clause_list


def visiterVerbe(token):
    clause_list = []
    for child in token.rights:
        if (child.dep_ == "conj"):
            # (nsubj)  (verb) (conj vers NOUN)
            clause_list = clause_list + \
                visiter_regle(token, child, ["nsubj"], ["conj"], ["NOUN"])
        if (child.dep_ == "dobj"):
            # (nsubj)  (verb) (dobj vers NOUN)
            clause_list = clause_list + \
                visiter_regle(token, child, ["nsubj"], ["dobj"], ["NOUN"])
        if (child.dep_ == "prep"):
            # nsubjpass (VERB) prep vers ADP
            clause_list = clause_list + \
                visiter_regle(token, child, ["nsubjpass"], ["prep"], ["ADP"])
            # nsubjpass (VERB) prep vers SCONJ
            clause_list = clause_list + \
                visiter_regle(token, child, ["nsubjpass"], ["prep"], ["SCONJ"])
        if (child.dep_ == "attr"):
            # PRON<-expl|nsubj- AUX -attr->NOUN
            clause_list = clause_list + \
                visiter_regle(token, child, ["expl", "nsubj"], [
                              "attr"], ["NOUN"])
    return clause_list


def extract_clauses(sentence_array):
    clause_list = []
    for sentence in sentence_array:
        for token in nlp(sentence.text):
            if (token.pos_ == "VERB" or token.pos_ == "AUX"):  # aux ?
                clause_list = clause_list+visiterVerbe(token)
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
        print("search2")
        if search(word, c.text):
            print("search")
            return c.text
    return "not found"


def replace_wh_words(sentence_nlp):
    new_text = ""
    last_subject = "undefined"
    for token in sentence_nlp:
        if token.dep_ == "pobj":
            last_subject = token.text
        if token.tag_ == "WDT" and not token.i == 0:
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


def preprocessing(sentences):
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace("-", '')
        sentences[i] = sentences[i].replace(",", '')
    return sentences


def generate(text):
    """
    Generate and return a set of boolean questions.
    """
    text = replace_wh_words(text)
    document = nlp(text)
    sentences = document.sents
    sentences += extract_clauses(sentences)
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
