from dis import Instruction
import enum
import itertools
import json
import re
from typing import Type
# from colorama import Fore, Back, Style, init
from dataclasses import dataclass
from xxlimited import Null

# init(autoreset=True)


class highlight_types(enum.Enum):
    web = "web"
    text = "text"


@dataclass
class configuration:
    state: str
    position: int
    text_version: int
    end_of_cycle: bool = False
    father: Type["configuration"] = None
    highlight = {"web": ["<b>", "</b>"], "text": ["(", ")"]}

    def __str__(self):
        return f"state: {self.state}, position: {self.position},\
         text_version: {self.text_version} "

    def stringify(self, text: list, size_of_window: int, output):
        type_of_highlight = highlight_types.web
        if output == print:
            type_of_highlight = highlight_types.text

        list_of_text = [i for i in text]
        start_bold = self.position
        end_bold = min(self.position + size_of_window-1, len(list_of_text) - 1)
        list_of_text[start_bold] = self.highlight[type_of_highlight.value][0] + \
            list_of_text[start_bold]
        list_of_text[end_bold] = list_of_text[end_bold] + \
            self.highlight[type_of_highlight.value][1]

        return ", ".join(list_of_text)


class OutputMode(enum.Enum):
    INSTRUCTIONS = 3
    CYCLES = 2
    RESULT = 1


class BaseAutomaton:
    initial_state = None
    size_of_window = 1
    special_instructions = ["MVL", "MVR", "[]"]
    out = OutputMode.INSTRUCTIONS
    configs = []
    alphabet = set()
    working_alphabet = set()
    special_symbols = "#$*"
    name = "Automaton"
    type = "RLWW"
    doc_string = ""
    instructions = {}
    output = False
    logs = ""

    def __init__(self, file="", out_mode=OutputMode.INSTRUCTIONS, output=False):
        self.out = out_mode
        self.output = output
        if file:
            try:
                self.load_from_json_file(file)
            except (FileNotFoundError, FileExistsError):
                self.log(2, "\nAutomaton can not be loaded")

    def log(self, importance, message, end="\n"):
        if self.out.value >= importance:
            if self.output:
                print(message, end=end)
            self.logs += str(message) + end

    @property
    def definition(self):
        return {
            "initial_state": self.initial_state,
            "alphabet": list(self.alphabet),
            "working_alphabet": list(self.working_alphabet),
            "size_of_window": self.size_of_window,
            "name": self.name,
            "type": self.type,
            "doc_string": self.doc_string,
            "instructions": self.instructions,
        }

    def load_from_json_file(self, file: str):
        with open(file, mode="r") as imported_file:
            self.load(json.load(imported_file))

    def load(self, definition: dict):
        self.initial_state = definition["initial_state"]
        self.alphabet = set(definition["alphabet"])
        self.working_alphabet = definition["working_alphabet"]
        self.size_of_window = int(definition["size_of_window"])
        self.name = definition["name"]
        self.type = definition["type"]
        self.doc_string = definition["doc_string"]
        self.instructions = definition["instructions"]

    def clear(self):
        self.log(2, "Loading clear automaton,")
        self.log(2, "Init State is 'st0' and window size is set to 1")
        self = BaseAutomaton()

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

    def __initialize_instructions(self, from_state, content_of_window):

        if from_state not in self.instructions:
            self.instructions[from_state] = {content_of_window: []}

        if content_of_window not in self.instructions[from_state]:
            self.instructions[from_state][content_of_window] = []

    def substituted_dots_in_window(self, window):
        r = [window]
        while any(["." in w for w in r]):
            r = [word.replace(".", symbol, 1)
                 for symbol in self.alphabet for word in r]
        return r

    def __check_used_symbols(self, word):
        return True

    def add_instr(self, from_state: str, content_of_window, to_state: str, instruction: str):
        for window in self.substituted_dots_in_window(content_of_window):
            if not type(window) is list:
                window = str(list(window))
            self.__initialize_instructions(from_state, window)
            if instruction not in self.special_instructions:
                instruction = str(self.__parse_text_to_list(instruction))
            self.instructions[from_state][window].append(
                [to_state, instruction])

    def add_one_instr(
            self, from_state: str, content_of_window, instruction) -> bool:
        """
        Does not rewrite if exist, see replace_instruction
        modify delta[from_state, value] -> [to_state, instruction] | Accept | Restart
        return False if instruction exists / True otherwise
        """
        for window in self.substituted_dots_in_window(content_of_window):
            if not type(window) is list:
                window = str(list(window))
            self.__initialize_instructions(from_state, window)
            self.instructions[from_state][window].append(
                instruction)

    # def replace_instructions(self, from_state, value, to_state, instruction):
    #     self.instructions[from_state][value] = [[to_state, instruction]]

    def __do_instruction(self, right_side, stat: configuration):
        position = stat.position
        end_position = self.size_of_window + position
        text_version = stat.text_version
        restarted = False
        accepted = False
        to_state = Null
        if type(right_side) is str:
            if right_side == "Restart":
                position = 0
                restarted = True
                to_state = self.initial_state
            elif right_side == "Accept":
                accepted = True
        elif type(right_side) is list and len(right_side) == 2:
            to_state = right_side[0]
            instruction = right_side[1]
            if instruction == "MVR":
                position += 1
            elif instruction == "MVL":
                position -= 1
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
        if not accepted:
            new_conf = configuration(
                state=to_state, position=position, text_version=text_version, end_of_cycle=restarted, father=stat)
            self.configs.append(new_conf)
            return False
        else:
            return True

    def __move(self, window, conf: configuration):
        possible_windows = self.instructions[conf.state]
        if "['*']" in possible_windows:
            for right_side in possible_windows["['*']"]:
                if self.__do_instruction(right_side, conf):
                    return True
        elif window in possible_windows.keys():
            for right_side in possible_windows[window]:
                if self.__do_instruction(right_side, conf):
                    return True
        return False

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
                self.log(2, config.stringify(
                    text, self.size_of_window, output=self.output))
            else:
                self.log(3, config.stringify(
                    text, self.size_of_window, output=self.output))

    def dfs_search(self, configs):
        pass

    def bfs_search(self):
        while self.configs:
            conf = self.configs.pop()
            window = self.__get_window(
                self.texts[conf.text_version], conf.position)
            if self.__move(window, conf):
                self.log(2, f"remaining tuples = {self.configs}")
                self.log(
                    2, f"number of copies of text = {len(self.texts)}")
                self.pretty_printer(conf)
                return True
        return False

    def evaluate(self, word) -> bool:
        self.texts = [self.__parse_text_to_list(word)]
        self.paths_of_stats = [[0]]
        starting_status = configuration(
            self.initial_state, 0, 0)
        self.configs = [starting_status]
        self.log(2, self.texts[0])
        return self.bfs_search()

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
        self.working_alphabet = sorted(self.working_alphabet)
        with open(to, "w") as to_file:
            json.dump(self.definition, to_file)

    def is_deterministic(self):
        for state in self.instructions:
            for value in self.instructions[state]:
                if len(self.instructions[state][value]) > 1:
                    return False
        return True
