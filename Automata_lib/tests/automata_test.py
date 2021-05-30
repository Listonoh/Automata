# from automata import Automaton
from Automata_lib import Automaton, Text_Automaton
import json
import filecmp
import sys
txt_in = "Automata_lib/tests/Examples/Example0/Example0.txt"
json_out = "Automata_lib/tests/Examples/Example0/Example0_out.json"
json_in = "Automata_lib/tests/Examples/Example0/Example0.json"
txt_out = "Automata_lib/tests/Examples/Example0/Example0_out.txt"


def __compare_json(file1, file2):
    with open(file1, "r") as open_file1:
        with open(file2, "r") as open_file2:
            return json.load(open_file1) == json.load(open_file2)


def test_11():
    a = Automaton()
    definition = a.definition
    assert definition == a.definition


def test_from_text_to_json():
    a = Text_Automaton()
    a.load_text(txt_in)
    a.save_instructions(json_out)
    filecmp.clear_cache()
    assert __compare_json(json_out, json_in)


def test_from_json_to_text():
    a = Text_Automaton()
    a.load_from_json_file(json_in)
    a.save_text(txt_out)

    filecmp.clear_cache()
    assert filecmp.cmp(txt_in, txt_out)


def test_from_json_to_json():
    a = Automaton(file=json_in)
    a.save_instructions(json_out)

    filecmp.clear_cache()
    assert __compare_json(json_out, json_in)


def test_from_text_to_text():
    a = Text_Automaton()
    a.load_text(txt_in)
    a.save_text(txt_out)

    filecmp.clear_cache()
    assert filecmp.cmp(txt_in, txt_out)


def test_accepting_word():
    a = Text_Automaton()
    a.load_text(txt_in)
    assert a.evaluate("#aaabbbc$")
    assert a.evaluate("#aaabbbbbbd$")
    assert not a.evaluate("#aaabbbbb$")
