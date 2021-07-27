from Automata_lib import Automaton, OutputMode

# accept language { a^n b^n c | n >= 0 } union { a^n b^2n d | n >= 0}

a = Automaton(output=print, out_mode=OutputMode.INSTRUCTIONS)

a.size_of_window = 3
a.initial_state = "q0"
a.add_to_alphabet("a", "b", "c", "d")

for i in ["aaa", "aab", "abb", "abc", "bbb", "bbc", "bbd"]:
    a.add_instr("q0", i, "q0", "MVR")

a.add_one_instr("q0", "#c$", "Accept")
a.add_one_instr("q0", "#d$", "Accept")

a.add_instr("q0", "#ab", "q0", "MVR")
a.add_instr("q0", "#aa", "q0", "MVR")
a.add_instr("q0", "bc$", "qc", "MVL")
a.add_instr("q0", "bd$", "qd", "MVL")

a.add_one_instr("qr", "*", "Restart")

a.add_instr("qc", "abc", "qr", "c")
a.add_instr("qc", "bbc", "qc", "MVL")
a.add_instr("qc", "bbb", "qc", "MVL")
a.add_instr("qc", "abb", "qr", "b")
a.add_instr("qd", "bbd", "qd", "MVL")
a.add_instr("qd", "bbb", "qd", "MVL")
a.add_instr("qd", "abb", "qr", "[]")

# print(a.alphabet)

print(a.evaluate("#aaabbbc$"))  # True
input()
print(a.evaluate("#aaabbbbbbd$"))  # True
input()
print(a.evaluate("#aaabbbbb$"))  # False
