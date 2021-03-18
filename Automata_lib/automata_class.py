import itertools
import json
import re
from typing import Type
# from colorama import Fore, Back, Style, init
from dataclasses import dataclass

# init(autoreset=True)


@dataclass
class configuration:
    state: str
    position: int
    text_version: int
    father: Type["configuration"] = None

    def __str__(self):
        return f"state: {self.state}, position: {self.position},\
         text_version: {self.text_version} "


class Automaton:
    out = 4
    configs = []
    starting_state = "st0"
    starting_position = 0
    alphabet = set()
    accepting_states = set("st0")
    size_of_window = 1
    name = "Clear automaton"
    type = "None"
    doc_string_for_instance_of_automaton = "This is clear automaton"
    instructions = {}
    output = False
    logs = ""

    def __init__(self, file="", out_mode=4, output=False):
        self.out = out_mode
        self.output = output
        if file:
            try:
                self.log(2, "------------Loading------------")
                with open(file, mode='r') as inported_file:
                    self.definition = json.load(inported_file)
                self.log(
                    2, "Automaton loaded\n----------------------------------")
            except (FileNotFoundError, FileExistsError):
                self.log(
                    2, "\nAutomaton can not be loaded\
                        \n----------------------------------")
                return

    def log(self, importance, message, end="\n"):
        if self.out >= importance:
            if self.output:
                self.output(message, end=end)
            self.logs += str(message) + end

    @property
    def definition(self):
        return {
            "state0": self.starting_state,
            "position0": self.starting_position,
            "alphabet": list(self.alphabet),
            "sAcc": list(self.accepting_states),
            "size_of_window": self.size_of_window,
            "name": self.name,
            "type": self.type,
            "doc_string": self.doc_string_for_instance_of_automaton,
            "instructions": self.instructions,
        }

    def load(self, definition: dict):
        self.starting_state = definition["state0"]
        self.starting_position = definition["position0"]
        self.alphabet = set(definition["alphabet"])
        self.accepting_states = set(definition["sAcc"])
        self.size_of_window = definition["size_of_window"]
        self.name = definition["name"]
        self.type = definition["type"]
        self.doc_string_for_instance_of_automaton = definition["doc_string"]
        self.instructions = definition["instructions"]

    def clear(self):
        self.log(
            2, "Loading clear automaton, \n Init State is 'st0' and window\
                 size is set to 1 \n Accepting state is 'st0'")
        self.starting_state = "st0"
        self.starting_position = 0
        self.alphabet = set()
        self.accepting_states = set("st0")
        self.size_of_window = 1
        self.name = "Clear automaton"
        self.type = "None"
        self.doc_string_for_instance_of_automaton = "This is clear automaton"
        self.instructions = {}

    def add_to_alphabet(self, *chars):
        for ch in chars:
            self.alphabet.add(ch)

    def add_accepting_state(self, *states):
        for state in states:
            self.accepting_states.add(state)

    # TODO
    def get_words_of_len(self, length=5, count=20):
        return None
        return_arr = []
        for possibility in itertools.product(self.alphabet, length):
            if True:
                return_arr.append(possibility)
            if len(return_arr) >= count:
                return return_arr
        return return_arr

    def __make_instruction(self, instruction: str,
                           new_state: str, stat: configuration):
        position = stat.position
        end_position = self.size_of_window + position

        if instruction == "MVR":
            conf = configuration(new_state, position + 1,
                                 stat.text_version, stat)
            self.configs.append(conf)
        elif instruction == "MVL":
            conf = configuration(new_state, position - 1,
                                 stat.text_version, stat)
            self.configs.append(conf)
        elif instruction == "Restart":
            conf = configuration(new_state, 0, stat.text_version, stat)
            self.configs.append(conf)
        elif instruction == "Accept":
            conf = configuration(new_state, 0, stat.text_version, stat)
            self.configs.append(conf)
        # matching rewrites, for remove use "[]"
        elif re.match(r"^\[.*\]$", instruction):
            # new copy of current state
            new_list = self.texts[stat.text_version].copy()
            new_values = eval(instruction)  # making array from string
            new_list[position: end_position] = new_values  # rewriting

            self.texts.append(new_list)
            conf = configuration(new_state, stat.position,
                                 len(self.texts) - 1, stat)
            self.configs.append(conf)
        return

    def add_instr(self, from_state: str, value, to_state: str,
                  instruction: str, value_as_list: bool = False) -> bool:
        """
        Does not rewrite if exist, see replace_instruction
        modify delta[from_state, value] -> [state, instruction]
        return False if instruction exists / True otherwise
        """
        if not value_as_list:
            value = str(list(value))
        if from_state not in self.instructions:
            self.instructions[from_state] = {value: []}

        if value not in self.instructions[from_state]:
            self.instructions[from_state][value] = []
        if [to_state, instruction] in self.instructions[from_state][value]:
            return False
        self.instructions[from_state][value].append([to_state, instruction])
        return True

    def replace_instructions(self, from_state, value, to_state, instruction):
        self.instructions[from_state][value] = [
            [to_state, instruction]]

    def __move(self, window, conf):
        possibilities = self.instructions[conf.state]
        if "['*']" in possibilities:  # for all possibilities do this
            for possibility in possibilities["['*']"]:
                self.log(2, ">instruction: * -> new_state: ***")
                self.__make_instruction(possibility[1], possibility[0], conf)
        for possibility in possibilities[window]:
            self.log(
                2, f">instruction: {window} -> new_state: {possibility[0]},\
                     instruction: {possibility[1]}  ")
            self.__make_instruction(possibility[1], possibility[0], conf)
        self.log(2, "----------------------------------\n")

    def __get_window(self, text, position):
        end_of_pos = position + self.size_of_window
        return str(text[position:end_of_pos])

    def __parse_text_to_list(self, text):
        parsed_text = []
        ctr = 0
        working_string = ""
        for i in text:
            if i == "[":
                ctr += 1
            elif i == "]":
                ctr -= 1
            working_string += i
            if ctr == 0:
                parsed_text.append(working_string)
                working_string = ""
        if ctr != 0:
            raise Exception("[] are not in pairs")
        return parsed_text

    def pretty_printer(self, config: configuration):
        if config is None:
            return
        else:
            self.pretty_printer(config.father)
            text = self.texts[config.text_version]

            self.log(3, "[", end="")
            for i in range(len(text)):
                if config.position <= i < config.position + self.size_of_window:
                    # self.log(3, Fore.RED + str(text[i]), end="")
                    self.log(3, "<b>" + str(text[i]) + "</b>", end="")
                else:
                    self.log(3, str(text[i]), end="")
                if i < len(text):
                    self.log(3, ", ", end="")
            self.log(3, f"] {config.state}")

    def iterate_text(self, text):
        self.texts = [self.__parse_text_to_list(text)]
        self.paths_of_stats = [[0]]
        starting_status = configuration(
            self.starting_state, self.starting_position, 0)
        self.configs = [starting_status]
        self.log(2, self.texts[0])
        while True:
            try:
                conf = self.configs.pop()
                if conf.state == "Accept":
                    raise Exception("Accepting state")
                self.log(2, f"     > taking status : {conf}")
                window = self.__get_window(
                    self.texts[conf.text_version], conf.position)
                self.log(2, f" text: {self.texts[conf.text_version]}")
                self.log(2, f" window: {window}")

                self.__move(window, conf)
            except:
                if conf.state in self.accepting_states:
                    self.log(2, f"remaining tuples = {self.configs}")
                    self.log(
                        2, f"number of copies of text = {len(self.texts)}")
                    self.pretty_printer(conf)
                    return True
                elif self.configs.__len__() == 0:
                    return False
        return "Error shouldn't get here"

    def print_instructions(self):
        for state in self.instructions:
            print(f"states: {state}: <", end="")
            for value in self.instructions[state]:
                print(f" \"{value}\" : [", end="")
                for instruct in self.instructions[state][value]:
                    print(f"{instruct}", end="")
                print("]")
            print(">")

    def save_instructions(self, to):
        with open(to, "w") as to_file:
            json.dump(self.definition, to_file)

    def is_deterministic(self):
        for state in self.instructions:
            for value in self.instructions[state]:
                if len(self.instructions[state][value]) > 1:
                    return False
        return True

    def to_text(self, file):
        with open(file, "w") as out_file:
            for key, value in self.definition.items():
                if key != "instructions":
                    if type(value) is list:
                        out_file.write("{}: {}\n".format(
                            key, ", ".join(value)))
                    else:
                        out_file.write("{}: {}\n".format(key, value))
                else:
                    for state, instructions in value.items():
                        for window, possible_outcomes in instructions.items():
                            for new_state, instruction in possible_outcomes:
                                sting_window = "".join(item[1:-1] for item in
                                                       window[1:-1].split(", "))
                                out_file.write(
                                    "{} {} -> {} {}\n".format(state, sting_window, new_state, instruction))
