#!/usr/bin/env python3

# pylint: disable=C0114, C0116
import json
import pickle


def read_verbs() -> list[dict]:
    entries = []
    with open("data/verb.json", "r", encoding="utf-8") as json_file:
        for line in json_file:
            word_entry = json.loads(line)
            entries.append(word_entry)
    return entries


def concatenate(iterable: list, sep=",") -> str:
    res = iterable[0]
    for s in iterable[1:]:
        res += sep + s
    return res


def is_good_word(entry: dict, good_words: list[str]) -> bool:
    if entry["word"] in good_words:
        return True
    return False


def select_conjugation(entry: dict) -> dict[str, str]:
    my_tags = ["indicative", "present"]
    conjs = {
        "verb": entry["word"],
    }
    for form in entry["forms"]:
        if all(tag in form["tags"] for tag in my_tags):
            new_key = [t for t in form["tags"] if t not in my_tags]
            new_key = concatenate(new_key)
            conjs[new_key] = form["form"]
    return conjs


def construct_conj_table(entries: list[dict]) -> list[dict]:
    conjs = []

    good_words = []
    with open("data/good_words.txt", encoding="utf-8") as f:
        for line in f:
            good_words.append(line.strip())

    for entry in entries:
        if is_good_word(entry, good_words):
            conjs.append(select_conjugation(entry))
    return conjs


def create_conj_db():
    entries = read_verbs()
    conjs = construct_conj_table(entries)
    fname = "verb_dict.pyobj"

    with open("data/" + fname, "wb") as f:
        pickle.dump(conjs, f)


if __name__ == "__main__":
    create_conj_db()
