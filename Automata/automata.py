import itertools
import json
import re
import os
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)


class status:
    def __init__(self, state, position: int, text_version, father=None):
        self.state, self.position, self.text_version = state, position, text_version
        self.father = father

    def __str__(self):
        return f"state: {self.state}, position: {self.position}, text_version: {self.text_version} "


class Automaton:

    def clear(self):
        print(
            f"Loading clear automaton, \n Init State is 'st0' and window size is set to 1 \n Accepting state is 'st0' ") if self.out % 2 == 0 else None
        self.definition = {"s0": ["st0", 0],
                           "alphabet": [],
                           "sAcc": ["st0"],
                           "size_of_window": 1,
                           "name": "Clear automaton",
                           "type": "None",
                           "doc_string": "Some documentation for this automaton. This is clear automaton",
                           "instructions": {}
                           }

    def __init__(self, file="", out=3):
        self.out = out
        print("------------Loading--------------") if self.out % 2 == 0 else None
        if file == "":
            self.clear()
        else:
            with open(file, mode='r') as inp:  # load data from json file
                self.definition = json.load(inp)
        print(f"Automaton loaded") if self.out % 2 == 0 else None
        print("----------------------------------") if self.out % 2 == 0 else None

    def is_in_alphabet(self, ch):
        if ch in self.definition["alphabet"]:
            return True
        return False

    def add_to_alphabet(self, *chars):  # going to be internal
        for ch in chars:
            if not ch in self.definition["alphabet"]:
                self.definition["alphabet"].append(ch)

    def add_accepting_state(self, *states):
        for st in states:
            if st not in self.definition["sAcc"]:
                self.definition["sAcc"].append(st)

    def is_accepting_state(self, state):
        if state in self.definition["sAcc"]:
            return True
        return False

    def get_words_of_len(self, lenght=5, count=20):
        return_arr = []
        for possibility in itertools.product(self.definition["alphabet"], lenght):
            if True:
                return_arr.append(possibility)
            if len(return_arr) >= count:
                return return_arr
        return return_arr

    def get_words_of_length(self, length=5, count=20):
        retarr = []
        for possibility in itertools.product(self.mess["alphabet"], length):
            if True:
                retarr.append(possibility)
            if len(retarr) >= count:
                return retarr
        return retarr

    def __make_instruction(self, instruction, new_state, stat):
        pos = stat.position
        end_of_pos = self.size_of_window + pos

        if instruction == "MVR":  # move right
            s = status(new_state, pos + 1, stat.text_version, stat)
            self.stats.append(s)
        elif instruction == "MVL":  # move right
            s = status(new_state, pos - 1, stat.text_version, stat)
            self.stats.append(s)
        elif instruction == "Restart":  # restart
            s = status(new_state, 0, stat.text_version, stat)
            self.stats.append(s)
        elif instruction == "Accept":  # restart
            s = status(new_state, 0, stat.text_version, stat)
            self.stats.append(s)
        elif re.match(r"^\[.*\]$", instruction):  # matching rewrites, for remove use "[]"
            new_list = self.texts[stat.text_version].copy()  # new copy of curent state
            new_values = eval(instruction)  # making array from string
            new_list[pos: end_of_pos] = new_values  # rewriting

            self.texts.append(new_list)
            s = status(new_state, stat.position, len(self.texts) - 1, stat)
            self.stats.append(s)
        return

    def add_instr(self, from_state: str, value, to_state: str, instruction: str, strtolist: bool = False) -> bool:
        """
        Does not rewrite if exist, see replace_instruction
        modify delta[from_state, value] -> [state, instruction]
        return False if instruction exists / True otherwise
        """
        if strtolist:
            value = str(list(value))
        if from_state not in self.definition["instructions"]:
            self.definition["instructions"][from_state] = {value: []}
        if value not in self.definition["instructions"][from_state]:
            self.definition["instructions"][from_state][value] = []

        if [to_state, instruction] in self.definition["instructions"][from_state][value]:
            return False
        self.definition["instructions"][from_state][value].append([to_state, instruction])
        return True

    def replace_instructions(self, from_state, value, to_state, instruction):
        self.definition["instructions"][from_state][value] = [[to_state, instruction]]

    def __move(self, window, stat):
        possibilities = self.definition["instructions"][stat.state]
        if "['*']" in possibilities:  # for all possibilities do this
            for possibility in possibilities["['*']"]:
                print(f">instruction: * -> new_state: ***") if self.out % 2 == 0 else None
                self.__make_instruction(possibility[1], possibility[0], stat)
        for possibility in possibilities[window]:
            print(
                f">instruction: {window} -> new_state: {possibility[0]}, instruction: {possibility[1]}  ") if self.out % 2 == 0 else None
            self.__make_instruction(possibility[1], possibility[0], stat)
        print("----------------------------------", end="\n\n") if self.out % 2 == 0 else None

    def __get_window(self, text, position):
        end_of_pos = position + self.size_of_window
        return str(text[position:end_of_pos])

    def __concat_text(self, text):
        newtext = []
        ctr = 0
        strg = ""
        for i in text:
            if i == "[":
                ctr += 1
            elif i == "]":
                ctr -= 1
            strg += i
            if ctr == 0:
                newtext.append(strg)
                strg = ""
        if ctr != 0:
            raise ImportWarning("[] are not in pairs")
        return newtext

    def pretty_printer(self, stat: status):
        if stat is None:
            return
        else:
            self.pretty_printer(stat.father)
            text = self.texts[stat.text_version]
            i = 0
            b, e = stat.position, stat.position + self.size_of_window
            print("[", end="") if self.out % 3 == 0 else None
            while i < len(text):
                if b <= i < e:
                    print(Fore.RED + str(text[i]), end="") if self.out % 3 == 0 else None
                else:
                    print(str(text[i]), end="") if self.out % 3 == 0 else None
                i += 1
                if i < len(text):
                    print(", ", end="") if self.out % 3 == 0 else None
            print("]") if self.out % 3 == 0 else None

    def iterate_text(self, text):
        self.texts = [self.__concat_text(text)]
        self.paths_of_stats = [[0]]
        self.size_of_window = self.definition["size_of_window"]  # implicitly set to 1
        starting_status = status(self.definition["s0"][0], self.definition["s0"][1], 0)  # implicitly set to "st0" and 0
        self.stats = [starting_status]
        print(self.texts[0]) if self.out % 2 == 0 else None
        while True:
            try:
                s = self.stats.pop()
                if s.state == "Accept":
                    raise Exception("Accepting state")
                print(f"     > taking status : {s}") if self.out % 2 == 0 else None
                window = self.__get_window(self.texts[s.text_version], s.position)
                print(f" text: {self.texts[s.text_version]}") if self.out % 2 == 0 else None
                print(f" window: {window}") if self.out % 2 == 0 else None
                self.__move(window, s)
            except:
                if self.is_accepting_state(s.state):
                    print(f"remaining tuples = {self.stats}") if self.out % 2 == 0 else None
                    print(f"number of copies of text = {len(self.texts)}") if self.out % 2 == 0 else None
                    self.pretty_printer(s)
                    return True
                elif self.stats.__len__() == 0:
                    return False

    def print_instructions(self):
        for state in self.definition["instructions"]:
            print(f"states: {state}: <", end="")
            for value in self.definition["instructions"][state]:
                print(f" \"{value}\" : [", end="")
                for instruct in self.definition["instructions"][state][value]:
                    print(f"{instruct}", end="")
                print("]")
            print(">")

    def save_instructions(self, to):
        with open(to, "w") as to_file:
            json.dump(self.definition, to_file)

    def is_deterministic(self):
        for state in self.definition["instructions"]:
            for value in self.definition["instructions"][state]:
                if len(self.definition["instructions"][state][value]) > 1:
                    return False
        return True
