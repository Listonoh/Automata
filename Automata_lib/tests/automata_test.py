# from automata import Automaton
from Automata_lib import Automaton


def test_11():
    a = Automaton()
    definition = a.definition
    assert definition == a.definition
