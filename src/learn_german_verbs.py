#!/usr/bin/env python3

# pylint: disable=C0114, C0116
import pickle
import random
import difflib
import colorama

PRONOUNS = {
    ("singular", "first-person"): "ich",
    ("singular", "second-person"): "du",
    ("singular", "third-person"): "er/sie/es",
    ("plural", "first-person"): "wir",
    ("plural", "second-person"): "ihr",
    ("plural", "third-person"): "sie",
}

DIR_PATH = "/home/rbn/git/german_verb/"


def select_pronoun(conjugation: str) -> str:
    number, person = conjugation.split(",")
    if person in ("singular", "plural"):
        person, number = number, person

    return PRONOUNS[(number, person)]


def load_verbs() -> list:
    with open(DIR_PATH + "data/verb_dict.pyobj", "rb") as file:
        return pickle.load(file)


def diff_conjugation(user_input: str, correct: str) -> str:
    cl_save = colorama.Fore.GREEN
    cl_delete = colorama.Fore.RED
    cl_nill = colorama.Style.RESET_ALL

    result = ""

    differ = difflib.ndiff(user_input, correct)
    for d in differ:
        if d[0] == " ":
            result += cl_save + d[2] + cl_nill
        elif d[0] == "-":
            result += cl_delete + d[2] + cl_nill

    return result


def interactive_loop(verbs: list):
    cl_wrong = colorama.Fore.RED
    cl_correct = colorama.Fore.GREEN
    cl_good_word = colorama.Fore.BLUE
    cl_to_do = colorama.Fore.YELLOW
    cl_nill = colorama.Style.RESET_ALL

    while True:
        rand_entry = random.choice(verbs)
        rand_conjugation = random.choice(
            [key for key in rand_entry.keys() if key != "verb"]
        )
        print(f"Conjugate the verb {cl_to_do + rand_entry['verb'] + cl_nill}:")
        print(select_pronoun(rand_conjugation), " ", end="")

        try:
            user_input = input()
        except EOFError:
            break

        if user_input == "exit":
            break

        if user_input == rand_entry[rand_conjugation]:
            print(cl_correct + "Correct!" + cl_nill)
        else:
            diff_entry = diff_conjugation(user_input, rand_entry[rand_conjugation])
            print(
                cl_wrong + "Wrong!" + cl_nill,
                " The correct answer is",
                cl_good_word + rand_entry[rand_conjugation] + cl_nill,
                f"not {diff_entry}",
            )
        print()


if __name__ == "__main__":
    gverbs = load_verbs()
    print("Welcome to the German Verbs Learning Program™!")
    print("Let's practice conjugating German verbs.")
    print()
    interactive_loop(gverbs)
