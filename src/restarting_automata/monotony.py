import ast

from typing import Dict, Generator, Iterable, List, Set, Tuple, Union
from .automata_class import OutputMode
from .text_automata_class import Automaton
import re
from graphviz import Digraph
from itertools import permutations
from collections import defaultdict


def is_monotonic(a: Automaton, silent=False) -> bool:
    digraph = to_digraph(a)
    # rewrites = get_rewrites(a)
    rewrites = {}
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


def to_digraph(a: Automaton) -> Dict[str, List[str]]:
    """
    Takes automaton and returns his digraph
    in form of dict[str, List[str]]:
    {
        "state[window]": [state[window0], state[window1]],
        ...
    }
    """
    possible_states = set(
        ["Accept", "Restart"]
    )  # set of special instructions that could be in automaton as state

    for key, windows in a.instructions.items():
        for current_window in windows.keys():
            possible_states.add(key + current_window)

    possible_states = possible_states
    digraph = defaultdict(list)
    rewrites = defaultdict(list)

    digraph["Initial"] = [("", state) for state in possible_states if "#" in state]

    for state, transition_function in a.instructions.items():
        for from_window, instructions in transition_function.items():
            for instruction in instructions:
                valid_extensions = get_valid_extensions(
                    a, possible_states, from_window, instruction
                )
                current_state = state + from_window
                digraph[current_state] += valid_extensions

    return digraph


def get_valid_extensions(
    a: Automaton,
    possible_states: Set[str],
    from_window: str,
    instruction: Union[str, Tuple[str, str]],
):
    if type(instruction) is str:
        return [("", instruction)]
    if type(instruction) is list and len(instruction) == 2:
        to_state = instruction[0]
        instruction = instruction[1]
        if instruction == "MVR":
            rt = [
                (symbol, to_state + next_window)
                for symbol, next_window in get_next_window(a, from_window)
                if to_state + next_window in possible_states
            ]
            if to_state + "['*']" in possible_states:
                rt.append(("*", to_state + "['*']"))
            return rt
        elif instruction == "MVL":
            raise Exception("Not supported two-way automata")
        elif re.match(r"^\[.*\]$", instruction):
            return get_rewrite_windows(instruction, to_state, possible_states)


def get_next_window(a: Automaton, from_window: str) -> List[Tuple[str, str]]:
    window = ast.literal_eval(from_window)[1:]
    possible_symbols = a.alphabet + a.working_alphabet
    result = []

    if window[-1] == "$":
        result.append(("", str(window)))
    else:
        possible_symbols + ["$"]

    for c in possible_symbols:
        result.append((c, str(window + [c])))
    return result


def get_rewrite_windows(
    instruction: str, to_state: str, possible_states: Set[str]
) -> List[Tuple[str, str]]:
    """
    Takes part of the window + next state and go through all possible states if some matches.
    This should give us only O(n^2) where n is number of rewrite instructions
    """
    window = ast.literal_eval(instruction)

    incomplete_next_window = to_state + str(window)[:-1]
    # gets all possible_states that has prefix of incomplete_next_window
    result = [
        ("", possible_state)
        for possible_state in possible_states
        if incomplete_next_window in possible_state
    ]
    if to_state + "['*']" in possible_states:
        result.append(("*", to_state + "['*']"))
    return result


def from_digraph_to_dot(digraph: dict) -> Digraph:
    dot = Digraph()
    for from_state in digraph.keys():
        for label, to_state in digraph[from_state]:
            dot.edge(from_state, to_state, label)
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
