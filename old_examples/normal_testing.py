import automata as a


aut1 = a.automaton("data.json", 6)

aut1.replace_instructions("st0", "b", "st0", "MVR")
aut1.add_instruction("st0", "b", "st0", "MVR")
# aut1.print_instructions()
# aut1.save_instructions("data.1.json")
print(f"> deterministic: {aut1.is_deterministic()}")
text = "baa[a,b]aba"
print(f"iteratin {text}")
print("---------------------")
print(aut1.iterate_text(text))
