# from automata import Automaton
from Automata_lib import Automaton, Text_Automaton
import json
import filecmp
import sys
f1 = "Automata_lib/tests/Examples/Example0/Example0.txt"
f2 = "Automata_lib/tests/Examples/Example0/Example0_out.json"
f3 = "Automata_lib/tests/Examples/Example0/Example0.json"
f4 = "Automata_lib/tests/Examples/Example0/Example0_out.txt"


def __compare_json(file1, file2):
    open_file1 = open(file1, "r")
    open_file2 = open(file2, "r")
    return json.load(open_file1) == json.load(open_file2)


def test_11():
    a = Automaton()
    definition = a.definition
    assert definition == a.definition


def test_from_text_to_json():
    a = Text_Automaton()
    a.load_text(f1)
    a.save_instructions(f2)
    assert __compare_json(f2, f3)


def test_from_json_to_text():
    a = Text_Automaton(file=f3)
    a.save_text(f4)

    filecmp.clear_cache()
    assert filecmp.cmp(f1, f4)


def test_from_json_to_json():
    a = Automaton(file=f3)
    a.save_instructions(f2)

    assert __compare_json(f2, f3)


def test_from_text_to_text():
    a = Text_Automaton()
    a.load_text(f1)
    a.save_text(f4)

    filecmp.clear_cache()
    assert filecmp.cmp(f1, f4)


def test_accepting_word():
    a = Text_Automaton(file=f3)
    assert a.iterate_word("#aaabbbc$") and\
        a.iterate_word("#aaabbbbbbd$") and\
        not a.iterate_word("#aaabbbbb$")
