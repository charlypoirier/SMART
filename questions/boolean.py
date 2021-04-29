import spacy
from negspacy.negation import Negex
from negspacy.termsets import termset

def main():
    row1 = "She does not like Steve Jobs but likes Apple products."
    row2 = "There are three major types of rock: igneous, sedimentary, and metamorphic. The rock cycle is an important" \
           " concept in geology which illustrates the relationships between these three types of rock, and magma. " \
           "When a rock crystallizes from melt (magma and/or lava), it is an igneous rock. " \
           "This rock can be weathered and eroded, and then redeposited and lithified into a sedimentary rock, or be " \
           "turned into a metamorphic rock due to heat and pressure that change the mineral content of the rock which " \
           "gives it a characteristic fabric. The sedimentary rock can then be subsequently turned into a metamorphic " \
           "rock due to heat and pressure and is then weathered, eroded, deposited, and lithified, ultimately becoming" \
           " a sedimentary rock. Sedimentary rock may also be re-eroded and redeposited, and metamorphic rock may also " \
           "undergo additional metamorphism. All three types of rocks may be re-melted; when this happens, a new magma " \
           "is formed, from which an igneous rock may once again crystallize."
    # l = marking(row2)
    # negationForSpacy(row2)
    # print(l)
    nlp = spacy.load("en_core_web_sm")
    sentences_nlp_to_negate = nlp(row2)
    sentences_nlp_to_negate_list = list(sentences_nlp_to_negate.sents)
    print(len(sentences_nlp_to_negate_list))
    for s in sentences_nlp_to_negate_list:
        print(negate_verb_in_a_sentence(s))
    print(negate_verb_in_a_sentence(nlp("It looks good")))

    #sentence_to_negate = "She is the best in her domain."


def negate_aux_in_a_sentence(sentence_nlp_to_negate):
    new_sentence = ""
    for token in sentence_nlp_to_negate:
        if (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.pos_ == "AUX":
            new_sentence += token.text_with_ws + "not "
        else:
            new_sentence += token.text_with_ws
    return new_sentence


def negate_verb_in_a_sentence(sentence_nlp_to_negate):
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


def negationForSpacy(row):
    print("negation for spacy")
    nlp = spacy.load("en_core_web_sm")
    negex = Negex(nlp,
                  name="a",
                  neg_termset=termset("en_clinical").get_patterns(),
                  ent_types=["PERSON','ORG"],
                  extension_name="negex",
                  chunk_prefix=list())
    nlp.add_pipe("negex", config={"ent_types":["PERSON","ORG"]})
    doc = nlp(row)
    print(doc)
    for e in doc.ents:
        print(e.text, e._.negex, not e)

def marking(row):
    nlp = spacy.load("en_core_web_sm")
    chunks = []
    for token in nlp(row):
        if token.tag_ == 'VBZ':
            chunks.append('X' + token.whitespace_ + token.text + token.whitespace_)
        else:
            chunks.append(token.text_with_ws)
    res = "".join(chunks)
    return res

main()

"""
from questions.Question import Question
import spacy

nlp = spacy.load("en_core_web_sm")
"""
"""
Boolean questions
1) Negate the sentence
2) Replace an adjective with its synonym or antonym (https://pypi.org/project/spacy-wordnet/)
3) Replace pronouns with subject from last sentence
4) Extract subject-verb-complement
"""
""""
def generate(text):

    # Split into sentences
    document = nlp(text)
    sentences = document.sents

    # Generate questions
    questions = set()
    for sentence in sentences:
        question = Question(sentence.text, "True", ["False"])
        questions.add(question)

    return questions
"""
