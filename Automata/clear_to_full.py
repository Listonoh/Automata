from automata import automaton

a = automaton()

a.size_of_window = 2

a.add_to_alphabet("a")
a.add_to_alphabet("b")

a.add_instruction("st0", "['1']", "st1", "MVR")
a.add_instruction("st0", "['0']", "st0", "MVR")
a.add_instruction("st1", "['1']", "st0", "MVR")
a.add_instruction("st1", "['0']", "st1", "MVR")

a.iterateText("1011001")
