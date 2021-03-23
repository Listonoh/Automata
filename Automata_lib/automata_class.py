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
    end_of_cycle: bool = False
    father: Type["configuration"] = None
    highlight_start = '<b>'
    highlight_end = "</b>"

    def __str__(self):
        return f"state: {self.state}, position: {self.position},\
         text_version: {self.text_version} "

    def stringify(self, text: list, size_of_window):
        a = [text[i] for i in range(len(text))]
        start_bold = self.position
        end_bold = min(self.position + size_of_window-1, len(a) - 1)
        a[start_bold] = self.highlight_start + a[start_bold]
        a[end_bold] = a[end_bold] + self.highlight_end

        return ", ".join(a)


class OutputModes:
    INSTRUCTIONS = 1
    CYCLES = 2
    RESULT = 3


class Automaton:
    out = 1
    configs = []
    starting_state = "st0"
    starting_position = 0
    alphabet = set()
    accepting_states = set("st0")
    size_of_window = 1
    name = "Clear automaton"
    type = "None"
    doc_string = "This is clear automaton"
    instructions = {}
    output = False
    logs = ""

    def __init__(self, file="", out_mode=1, output=False):
        self.out = out_mode
        self.output = output
        if file:
            try:
                self.load_from_json_file(file)
            except (FileNotFoundError, FileExistsError):
                self.log(2, "\nAutomaton can not be loaded")

    def log(self, importance, message, end="\n"):
        # if importance in self.output_modes:
        #     pass
        if self.out >= importance:
            if self.output:
                print(message, end=end)
            self.logs += str(message) + end

    @property
    def definition(self):
        return {
            "starting_state": self.starting_state,
            "starting_position": self.starting_position,
            "alphabet": list(self.alphabet),
            "accepting_states": list(self.accepting_states),
            "size_of_window": self.size_of_window,
            "name": self.name,
            "type": self.type,
            "doc_string": self.doc_string,
            "instructions": self.instructions,
        }

    def load_from_json_file(self, file: str):
        with open(file, mode="r") as inported_file:
            self.load(json.load(inported_file))

    def load(self, definition: dict):
        self.starting_state = definition["starting_state"]
        self.starting_position = definition["starting_position"]
        self.alphabet = set(definition["alphabet"])
        self.accepting_states = set(definition["accepting_states"])
        self.size_of_window = definition["size_of_window"]
        self.name = definition["name"]
        self.type = definition["type"]
        self.doc_string = definition["doc_string"]
        self.instructions = definition["instructions"]

    def clear(self):
        self.log(2, "Loading clear automaton,")
        self.log(2, "Init State is 'st0' and window size is set to 1")
        self.log(2, "Accepting state is 'st0'")
        self = Automaton()

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

    def add_instr(
        self, from_state: str, window_value, to_state: str, instruction: str,
    ) -> bool:
        """
        Does not rewrite if exist, see replace_instruction
        modify delta[from_state, value] -> [state, instruction]
        return False if instruction exists / True otherwise
        """

        # normalize list
        if not type(window_value) is list:
            window_value = str(list(window_value))

        if from_state not in self.instructions:
            self.instructions[from_state] = {window_value: []}

        if window_value not in self.instructions[from_state]:
            self.instructions[from_state][window_value] = []
        if [to_state, instruction] in self.instructions[from_state][window_value]:
            return False
        self.instructions[from_state][window_value].append(
            [to_state, instruction])
        return True

    def replace_instructions(self, from_state, value, to_state, instruction):
        self.instructions[from_state][value] = [[to_state, instruction]]

    def __do_instruction(self, instruction: str, new_state: str, stat: configuration):
        position = stat.position
        end_position = self.size_of_window + position
        text_version = stat.text_version
        restarted = False

        if instruction == "MVR":
            position += 1
        elif instruction == "MVL":
            position -= 1
        elif instruction == "Restart":
            position = 0
            restarted = True
        elif instruction == "Accept":
            position = 0
        elif re.match(r"^\[.*\]$", instruction):
            # matching rewrites, for remove use "[]"
            # new copy of current state
            new_list = self.texts[stat.text_version].copy()
            new_values = eval(instruction)  # making array from string
            new_list[position:end_position] = new_values  # rewriting

            self.texts.append(new_list)
            text_version = len(self.texts) - 1
        else:
            raise Exception("unexpected instruction")
        new_conf = configuration(
            state=new_state, position=position, text_version=text_version, end_of_cycle=restarted, father=stat)
        self.configs.append(new_conf)

    def __move(self, window, conf: configuration):
        possibilities = self.instructions[conf.state]
        if "['*']" in possibilities:  # for all possibilities do this
            for possibility in possibilities["['*']"]:
                self.__do_instruction(possibility[1], possibility[0], conf)
        for possibility in possibilities[window]:
            self.__do_instruction(possibility[1], possibility[0], conf)

    def __get_window(self, text: str, position: int):
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
        if config:
            self.pretty_printer(config.father)
            text = self.texts[config.text_version]
            if config.end_of_cycle:
                self.log(2, config.stringify(text, self.size_of_window))
            else:
                self.log(3, config.stringify(text, self.size_of_window))

    def dfs_search(self, configs):
        pass

    def bfs_search(self, configs):
        pass

    def iterate_tape(self, tape) -> bool:
        self.texts = [self.__parse_text_to_list(tape)]
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
                window = self.__get_window(
                    self.texts[conf.text_version], conf.position)
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
                print(f' "{value}" : [', end="")
                for instruct in self.instructions[state][value]:
                    print(f"{instruct}", end="")
                print("]")
            print(">")

    def save_instructions(self, to):
        self.alphabet = sorted(self.alphabet)
        with open(to, "w") as to_file:
            json.dump(self.definition, to_file)

    def is_deterministic(self):
        for state in self.instructions:
            for value in self.instructions[state]:
                if len(self.instructions[state][value]) > 1:
                    return False
        return True
