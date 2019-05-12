from automata import automaton

a = automaton()
a.mess["size_of_window"]  = 3
a.mess["s0"] = ["q0", 0]
a.add_to_alphabet("#", "$", "a", "b", "c", "d")

a.add_accepting_state("Accept")

for i in ["aaa", "aab", "abb", "abc", "bbb", "bbc", "bbd"]:
    a.add_instruction("q0", i, "q0", "MVR", strtolist=True)

a.add_instruction("q0", "#c$", "Accept", "Accept", strtolist=True)
a.add_instruction("q0", "#d$", "Accept", "Accept", strtolist=True)

a.add_instruction("q0", "#ab", "q0", "MVR", strtolist=True)
a.add_instruction("q0", "#aa", "q0", "MVR", strtolist=True)
a.add_instruction("q0", "bc$", "qc", "MVL", strtolist=True)
a.add_instruction("q0", "bd$", "qd", "MVL", strtolist=True)

a.add_instruction("qr", "*", "q0", "Restart", strtolist=True)

a.add_instruction("qc", "abc", "qr", "['c']", strtolist=True)
a.add_instruction("qc", "bbc", "qc", "MVL", strtolist=True)
a.add_instruction("qc", "bbb", "qc", "MVL", strtolist=True)
a.add_instruction("qc", "abb", "qr", "['b']", strtolist=True)
a.add_instruction("qd", "bbd", "qd", "MVL", strtolist=True)
a.add_instruction("qd", "bbb", "qd", "MVL", strtolist=True)
a.add_instruction("qd", "bbb", "qr", "[]", strtolist=True)

a.iterateText("#aaabbbc$")