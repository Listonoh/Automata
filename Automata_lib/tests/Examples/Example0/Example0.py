from Automata_lib import Automaton, Text_Automaton

# accept language { a^n b^n c | n >= 0 } union { a^n b^2n d | n >= 0}

a = Text_Automaton(output=print, out_mode=3)

a.starting_position = 0
a.size_of_window = 3
a.initial_state = "q0"
a.add_to_alphabet("#", "$", "a", "b", "c", "d")

a.add_accepting_state("Accept")

for i in ["aaa", "aab", "abb", "abc", "bbb", "bbc", "bbd"]:
    a.add_instr("q0", i, "q0", "MVR")

a.add_instr("q0", "#c$", "Accept", "Accept")
a.add_instr("q0", "#d$", "Accept", "Accept")

a.add_instr("q0", "#ab", "q0", "MVR")
a.add_instr("q0", "#aa", "q0", "MVR")
a.add_instr("q0", "bc$", "qc", "MVL")
a.add_instr("q0", "bd$", "qd", "MVL")

a.add_instr("qr", "*", "q0", "Restart")

a.add_instr("qc", "abc", "qr", "['c']")
a.add_instr("qc", "bbc", "qc", "MVL")
a.add_instr("qc", "bbb", "qc", "MVL")
a.add_instr("qc", "abb", "qr", "['b']")
a.add_instr("qd", "bbd", "qd", "MVL")
a.add_instr("qd", "bbb", "qd", "MVL")
a.add_instr("qd", "abb", "qr", "[]")

print(a.alphabet)

print(a.evaluate("#aaabbbc$"))  # True
input()
print(a.evaluate("#aaabbbbbbd$"))  # True
input()
print(a.evaluate("#aaabbbbb$"))  # False
