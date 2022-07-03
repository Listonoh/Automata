from typing import Generator, List
from .automata_class import OutputMode
from .text_automata_class import Automaton
import re
from graphviz import Digraph
from itertools import permutations
from collections import defaultdict


def is_monotonic(a: Automaton, silent=False):
    digraph, rewrites = to_digraph(a)
    to_check = []
    for i in rewrites.keys():
        to_check.append(i)

    # check if nondeterministic could skip rewrite and rewrite later
    if __could_be_rewrite_far_apart(digraph, a, rewrites):
        return False

    # checking if in next run there could be rewrite in k-1-(|word|-|new_word|)
    if __could_be_rewrite_from_rewrite(digraph, a, rewrites):
        return False
    return True


def to_digraph(a: Automaton):
    possible_states = set(["Accept", "Restart"])
    for key in a.instructions.keys():
        for window in a.instructions[key]:
            possible_states.add(key + window)  # beware of star

    possible_states = list(possible_states)
    digraph = defaultdict(list)
    rewrites = defaultdict(list)

    digraph["Initial"] = [state for state in possible_states if "#" in state]
    extract_instructions(a, possible_states, digraph, rewrites)
    return digraph, rewrites


def extract_instructions(a, possible_states, digraph, rewrites):
    for key in a.instructions.keys():
        for window in a.instructions[key]:
            for instruction in a.instructions[key][window]:
                extract_instruction(
                    a, possible_states, key, window, digraph, rewrites, instruction
                )


def extract_instruction(
    a, possible_states, key, window, digraph, rewrites, instruction
):
    if type(instruction) is str:
        digraph[key + window].append(instruction)
    elif type(instruction) is list and len(instruction) == 2:
        to_state = instruction[0]
        instruction = instruction[1]
        if instruction == "MVR":
            extract_MVR(a, possible_states, key, window, digraph, to_state)
        elif instruction == "MVL":
            raise Exception("Not supported two-way automata")
        elif re.match(r"^\[.*\]$", instruction):
            extract_rewrite(
                possible_states, key, window, digraph, rewrites, instruction, to_state
            )


def extract_rewrite(
    possible_states, key, window, digraph, rewrites, instruction, to_state
):
    # rewrite_to = [a.strip() for a in instruction[1:-1].split(",")]
    # making array from string
    rewrite_to = eval(instruction)
    # if to_state+"['*']" in possible_states:
    #     tt = to_state+"['*']"
    #     rewrites[key+window].append({"rewriten_to":rewrite_to,"to_state": tt})
    #     digraph[key+window].append(tt)
    if rewrite_to and rewrite_to[-1] == "$":
        if to_state + "['$']" in possible_states:
            digraph[key + window].append(to_state + "['$']")
            rewrites[key + window].append(
                {"rewritten_to": rewrite_to, "to_state": to_state + "[]"}
            )
        else:
            for (
                possible_window
            ) in possible_states:  # get rid all that couldest be after ie those with #
                if (
                    "#" not in possible_window
                    and to_state == possible_window.split("[")[0]
                ):
                    digraph[key + window].append(possible_window)
                    rewrites[key + window].append(
                        {"rewritten_to": rewrite_to, "to_state": possible_window}
                    )


def extract_MVR(a, possible_states, key, window, digraph, to_state):
    for c in a.alphabet + a.working_alphabet + ["$"]:
        new_window = str(eval(window)[1:] + [c])
        if to_state + new_window in possible_states + [to_state + "['*']"]:
            digraph[key + window].append(to_state + new_window)


def from_digraph_to_dot(digraph: dict) -> Digraph:
    dot = Digraph()
    for from_state in digraph.keys():
        for to_state in digraph[from_state]:
            dot.edge(from_state, to_state)
    return dot


# def can_restart(state):
#     s = [state]
#     visited = [state]
#     possible_states = []
#     while s:
#         cur_state = s.pop()
#         for window in a.instructions[cur_state]:
#             for right_side in a.instructions[cur_state][window]:
#                 if right_side == "Accept":
#                     continue
#                 if right_side == "Restart":
#                     return True
#                 if right_side[0] not in visited:
#                     possible_states.append(right_side[0])
#                     visited.append(right_side[0])
#                     s.append(right_side[0])
#     return False


def generate_pre_complete_word(a: Automaton, content: list):
    return []
    final_length = a.size_of_window
    for i in range(1, len(content)):
        suffix = content[:i]
        symbols_needed = final_length - len(suffix) - 1
        perm = permutations(a.working_alphabet + a.alphabet, symbols_needed)
        for p in perm:
            for prefix in a.working_alphabet + a.alphabet + ["#"]:
                yield [prefix] + list(p) + suffix


def __could_be_rewrite_far_apart(digraph, a, rewrites):
    reversed_digraph = defaultdict(list)
    for key in digraph.keys():
        for item in digraph[key]:
            reversed_digraph[item].append(key)
            reversed_digraph[key]  # mark as visited

    used = {key: False for key in digraph.keys()}
    for state in rewrites.keys():
        st = [state]
        distance = {i: 0 if i == state else -1 for i in reversed_digraph.keys()}
        while st:
            current = st.pop(0)
            if distance[current] >= a.size_of_window and current in rewrites.keys():
                return True
            for next_state in reversed_digraph[current]:
                if distance[current] == float("inf"):
                    if not distance[next_state] == float("inf"):
                        distance[next_state] = float("inf")
                    else:
                        continue  # don't loop to infinity
                if distance[next_state] == -1:
                    distance[next_state] = distance[current] + 1
                else:
                    distance[next_state] = float("inf")
                st.append(next_state)


def __could_be_rewrite_from_rewrite(digraph, a, rewrites):
    accessible_from_initial = []
    to_check_without_states = [i[2:] for i in digraph.keys()]
    for i in digraph.keys():
        for rewrite in rewrites[i]:
            rewrite = rewrite["rewritten_to"]
            for possible_bad_state in generate_pre_complete_word(a, rewrite):
                if str(possible_bad_state) in to_check_without_states:
                    # if possible_bad_state in accessible_from_initial:
                    #     pass
                    # if not silent:
                    print(possible_bad_state, rewrite)
                    return True
    return False
