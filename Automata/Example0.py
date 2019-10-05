import sys

from automata import Automaton

# accept language { a^n b^n c | n >= 0 } union { a^n b^2n d | n >= 0}

a = Automaton()
a.definition["size_of_window"]  = 3
a.definition["s0"] = ["q0", 0]
a.add_to_alphabet("#", "$", "a", "b", "c", "d")

a.add_accepting_state("Accept")

for i in ["aaa", "aab", "abb", "abc", "bbb", "bbc", "bbd"]:
    a.add_instr("q0", i, "q0", "MVR", strtolist=True)

a.add_instr("q0", "#c$", "Accept", "Accept", strtolist=True)
a.add_instr("q0", "#d$", "Accept", "Accept", strtolist=True)

a.add_instr("q0", "#ab", "q0", "MVR", strtolist=True)
a.add_instr("q0", "#aa", "q0", "MVR", strtolist=True)
a.add_instr("q0", "bc$", "qc", "MVL", strtolist=True)
a.add_instr("q0", "bd$", "qd", "MVL", strtolist=True)

a.add_instr("qr", "*", "q0", "Restart", strtolist=True)

a.add_instr("qc", "abc", "qr", "['c']", strtolist=True)
a.add_instr("qc", "bbc", "q
c", "MVL", strtolist=True)
a.add_instr("qc", "bbb", "qc", "MVL", strtolist=True)
a.add_instr("qc", "abb", "qr", "['b']", strtolist=True)
a.add_instr("qd", "bbd", "qd", "MVL", strtolist=True)
a.add_instr("qd", "bbb", "qd", "MVL", strtolist=True)
a.add_instr("qd", "abb", "qr", "[]", strtolist=True)

print(a.iterate_text("#aaabbbc$"))  # true
sys.stdin.readline()
print(a.iterate_text("#aaabbbbbbd$"))  # True
sys.stdin.readline()
print(a.iterate_text("#aaabbbbb$"))  # False
