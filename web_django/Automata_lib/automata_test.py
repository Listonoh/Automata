from Automata_lib.automata import Automaton


def test_1():
    a = Automaton()
    definition = a.definition
    assert definition == a.definition
