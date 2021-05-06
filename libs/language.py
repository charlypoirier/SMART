"""
All language-related variables and functions,
accessible from anywhere where this is imported.
"""

import spacy
from PyDictionary import PyDictionary

# Spacy model (sm=faster, trf=slower)
nlp = spacy.load("en_core_web_trf")

# English dictionnary
dictionary = PyDictionary()

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
        left = []
        right = []
        for leftchild in token.lefts:
            left = cartesian_product(
                left, tt_combi_Obj(leftchild))
        for rightchild in token.rights:
            right = cartesian_product(
                right, tt_combi_Obj(rightchild))
        appendtokenToList(token, left, right)
        # right.append(vide)
        list_combi = cartesian_product(left, right)
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
        left = []
        right = []
        for leftchild in token.lefts:
            left = cartesian_product(
                left, tt_combi_Obj(leftchild))
        for rightchild in token.rights:
            right = cartesian_product(
                right, tt_combi_Obj(rightchild))
        appendtokenToList(token, left, right)
        list_combi = cartesian_product(left, right)
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
            clause_list.append(clause.strip())
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
                clause_list = clause_list + visiterVerbe(token)
    return set(preprocessing(clause_list))


def preprocessing(sentences):
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace("-", '')
        sentences[i] = sentences[i].replace(",", '')
        sentences[i] = sentences[i].replace(")", '')
        sentences[i] = sentences[i].replace("(", '')
        sentences[i] = sentences[i].replace("  ", ' ')
    return list(set(sentences))
