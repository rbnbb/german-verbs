import json
import logging
import pickle

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""Read wiktioanry data dump and return list of dict of words"""
def read_verbs():
    entries = []
    with open("data/verb.json") as json_file:
        for line in json_file:
            word_entry = json.loads(line)
            # logger.debug(f"{word_entry.keys()}")
            entries.append(word_entry)
    return entries

def concatenate(iterable, sep=','):
    res = iterable[0]
    for s in iterable[1:]:
        res += (sep + s)
    return res

"""return true if I want this word."""
def is_good_word(entry:dict):
    good_words = ["feien", "trinkst"]
    if entry["word"] in good_words:
        return True
    return False

def select_conjugation(entry):
    my_tags = ['indicative', 'present']
    conjs = {'verb': entry['word'],}
    j = 0
    for form in entry['forms']:
        if all([tag in form['tags'] for tag in my_tags]):
            new_key = [t for t in form['tags'] if t not in my_tags]
            new_key = concatenate(new_key)
            conjs[new_key] = form['form']
    return conjs


def construct_conj_table(entries):
    conjs = []
    for entry in entries:
        if is_good_word(entry):
            conjs.append(select_conjugation(entry))
    return conjs

def create_conj_db():
    entries = read_verbs()
    conjs = construct_conj_table(entries)
    fname = "verb_dict.pyobj"
    pickle.dumb(conjs, "../data/"+fname)


