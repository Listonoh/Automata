from automata import automaton
import sys

# accept language { a^n b^n c | n >= 0 } union { a^n b^2n d | n >= 0}

a = automaton(out=3)
a.mess["size_of_window"] = 3
a.mess["s0"] = ["q0", 0]  # seting starting state and position
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
a.add_instruction("qd", "abb", "qr", "[]", strtolist=True)
print(a.is_deterministic())
print(a.iterateText("#aaabbbc$"))
sys.stdin.readline()
print(a.iterate_text("#aaabbbbbbd$"))
sys.stdin.readline()
print(a.iterate_text("#aaabbbbb$"))
