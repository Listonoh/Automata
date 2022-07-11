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

    # edges from star
    for state, transition_function in a.instructions.items():
        for from_window, instructions in transition_function.items():
            if "*" in from_window:
                for instruction in instructions:
                    for configuration in possible_states:
                        if state == configuration[: len(state)]:
                            from_window = configuration[len(state) :]
                            valid_extensions = get_valid_extensions(
                                a, possible_states, from_window, instruction
                            )
                            digraph[configuration] += valid_extensions

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
            rt = []
            for symbol, next_window in get_next_window(a, from_window):
                if to_state + "['*']" in possible_states:
                    rt.append((symbol, to_state + next_window))
                    possible_states.add(to_state + next_window)

                elif to_state + next_window in possible_states:
                    rt.append((symbol, to_state + next_window))
            return rt

        elif instruction == "MVL":
            raise Exception("Not supported two-way automata")
        elif re.match(r"^\[.*\]$", instruction):
            return get_rewrite_windows(instruction, to_state, possible_states)


def get_next_window(a: Automaton, from_window: str) -> List[Tuple[str, str]]:
    """Takes automaton and window which may contain symbols or star and returns list of Edges"""
    if from_window == "['*']":
        """This is problematic becouse we don not know what symbols could be in window"""
        return []
    window = ast.literal_eval(from_window)[1:]
    possible_symbols = a.alphabet + a.working_alphabet
    result = []

    if window[-1] == "$":
        result.append(("", str(window)))
    else:
        possible_symbols += ["$"]

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
    # if to_state + "['*']" in possible_states:
    #     result.append(("*", to_state + "['*']"))
    return result


def from_digraph_to_dot(digraph: dict) -> Digraph:
    dot = Digraph()
    for from_state in digraph.keys():
        for label, to_state in digraph[from_state]:
            dot.edge(from_state, to_state, label)
    return dot
