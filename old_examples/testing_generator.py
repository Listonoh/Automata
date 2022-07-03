from automata import automaton

a = automaton()
a.add_to_alphabet("a", "b", "c")
print(a.get_words_of_lenght(5, 10))
