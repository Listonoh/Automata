from restarting_automata import BaseAutomaton, Automaton
import json
import filecmp

example_folder = "Examples/"

txt_in = f"{example_folder}Example0/Example0.txt"
json_out = f"{example_folder}Example0/Example0_out.json"
json_in = f"{example_folder}Example0/Example0.json"
txt_out = f"{example_folder}Example0/Example0_out.txt"


def __compare_json(file1, file2):
    with open(file1, "r") as open_file1:
        with open(file2, "r") as open_file2:
            return json.load(open_file1) == json.load(open_file2)


def test_11():
    a = BaseAutomaton()
    definition = a.definition
    assert definition == a.definition


def test_from_text_to_json():
    a = Automaton()
    a.load_text(txt_in)
    a.save_instructions(json_out)
    filecmp.clear_cache()
    assert __compare_json(json_out, json_in)


def test_from_json_to_text():
    a = Automaton()
    a.load_from_json_file(json_in)
    a.save_text(txt_out)

    filecmp.clear_cache()
    assert filecmp.cmp(txt_in, txt_out)


def test_from_json_to_json():
    a = BaseAutomaton(file=json_in)
    a.save_instructions(json_out)

    filecmp.clear_cache()
    assert __compare_json(json_out, json_in)


def test_from_text_to_text():
    a = Automaton(txt_in)
    a.save_text(txt_out)

    filecmp.clear_cache()
    assert filecmp.cmp(txt_in, txt_out)


def test_accepting_word():
    a = Automaton()
    a.load_text(txt_in)
    assert a.evaluate("aaabbbc")
    assert a.evaluate("aaabbbbbbd")
    assert not a.evaluate("aaabbbbb")


def test_0n1n():
    a = Automaton(example_folder + "0n1n.txt")
    results = [
        a.evaluate("000000111111"),
        not a.evaluate("00000111111"),
        a.evaluate("01"),
        a.evaluate("0011"),
        not a.evaluate("2000111"),
    ]
    assert sum(results) == 5


def test_brackets():
    a = Automaton(example_folder + "balanced_brackets.txt")
    results = [
        a.evaluate("((()())())"),
        not a.evaluate("())"),
        not a.evaluate("(()"),
        a.evaluate("()"),
        a.evaluate("()(())"),
        not a.evaluate("(2"),
    ]
    sum_results = sum(results)
    len_results = len(results)
    assert sum_results == len_results


def test_ending_01():
    a = Automaton(example_folder + "ending01.txt")
    results = [
        a.evaluate("10001100101"),
        not a.evaluate("0"),
        not a.evaluate(""),
        a.evaluate("0001"),
        a.evaluate("001101"),
        not a.evaluate("(2"),
    ]
    sum_results = sum(results)
    len_results = len(results)
    assert sum_results == len_results


def test_contain_01():
    a = Automaton(example_folder + "contain01.txt")
    results = [
        a.evaluate("10001100101"),
        not a.evaluate("1111110000"),
        not a.evaluate(""),
        a.evaluate("0001"),
        a.evaluate("001101"),
        not a.evaluate("(2"),
    ]
    sum_results = sum(results)
    len_results = len(results)
    assert sum_results == len_results


def test_example0_without_MVL():
    a = Automaton(example_folder + "example0_without_MVL.txt")
    results = [
        a.evaluate("abc"),
        not a.evaluate("aaac"),
        not a.evaluate(""),
        a.evaluate("aabbbbd"),
        a.evaluate("aaaabbbbbbbbd"),
        not a.evaluate("(2"),
    ]
    sum_results = sum(results)
    len_results = len(results)
    assert sum_results == len_results


def test_dot_to_words():
    a = Automaton()
    a.alphabet = ["1", "0"]
    b = a.substituted_dots_in_window("...")
    assert b == ["111", "011", "101", "001", "110", "010", "100", "000"]
