# import itertools
import json
import re
from colorama import Fore, Back, Style, init
init(autoreset=True)
class status:
    def __init__(self, state, position, text_version, father=None):
        self.state, self.position, self.text_version = state, position, text_version
        self.father = father

    def __str__(self):
        return f"state: {self.state}, position: {self.position}, text_version: {self.text_version} "


class automaton:
    def __init__(self, file=""):
        print("------------Loading--------------")
        if file == "":
            print(f"Loading clear automaton, \n Init State is 'st0' and window size is set to 1 \n Accepting state is 'st0' ")
            with open("clear_automaton.json", mode='r') as inp:  # load data from json file
                self.mess = json.load(inp)    
        else:
            with open(file, mode='r') as inp:  # load data from json file
                self.mess = json.load(inp)
        print(f"Automaton loaded")
        print("----------------------------------")


    def is_in_alphabet(self, ch):
        if ch in self.mess["alphabet"]:  
            return True
        return False

    def add_to_alphabet(self, ch): # going to be internal
        if not ch in self.mess["alphabet"]:
            self.mess["alphabet"].append(ch)


    def is_accepting_state(self, state):
        if state in self.mess["sAcc"]:
            return True
        return False       


    def __make_instruction(self, instruction, new_state, stat):
        pos = stat.position
        end_of_pos = self.size_of_window + pos

        if instruction == "MVR": # move right
            s = status(new_state, pos + 1, stat.text_version, stat)
            self.stats.append(s)
            return
        elif instruction == "RES": # restart
            s = status(new_state, 0, stat.text_version, stat)
            self.stats.append(s)
            return
        elif re.match(r"^\[.*\]$", instruction):    #matching rewrites, for remove use "[]"
            new_list = self.texts[stat.text_version].copy()     # new copy of curent state
            new_values = eval(instruction)                      # making array from string
            new_list[pos: end_of_pos] = new_values              # rewriting 

            self.texts.append(new_list)
            s = status(new_state, stat.position, len(self.texts) -1, stat)
            self.stats.append(s)
            return
        # else nothing its not deterministic


    def add_instruction(self, from_state, value, to_state, instruction):
        """
        Does not rewrite if exist, see replace_instruction
        modify delta[from_state, value] -> [state, instruction]
        return False if instruction exists / True otherwise
        """
        if not from_state in self.mess["instructions"]:
            self.mess["instructions"][from_state] = {value : []}
        if not value in self.mess["instructions"][from_state]:
            self.mess["instructions"][from_state][value] = []
            
        if [to_state, instruction] in self.mess["instructions"][from_state][value]:
            return False
        self.mess["instructions"][from_state][value].append([to_state, instruction])
        return True

    def replace_instructions(self, from_state, value, to_state, instruction):
        self.mess["instructions"][from_state][value] = [[to_state, instruction]]

    def __move(self, window, stat):
        posibilites = self.mess["instructions"][stat.state]
        for posibility in posibilites[window]:
            print(f">instruction: {window} -> new_state: {posibility[0]}, instruction: {posibility[1]}  " )
            self.__make_instruction(posibility[1], posibility[0], stat)
        print("----------------------------------", end="\n\n")
            

    def __get_window(self, text, position):
        end_of_pos = position + self.size_of_window
        return str(text[position:end_of_pos])

    def __concat_text(self, text):
        newtext = []
        ctr = 0
        strg = ""
        for i in text:
            if i == "[": ctr +=1
            elif i == "]": ctr -=1
            strg += i
            if ctr == 0:
                newtext.append(strg)
                strg = ""
        if ctr != 0:
            raise ImportWarning("[] are not in pairs")
        return newtext


    def prety_print(self, stat: status):
        if stat == None:
            return
        else:
            self.prety_print(stat.father)
            text = self.texts[stat.text_version]
            i=1
            b, e = stat.position, stat.position + self.size_of_window +1
            print("[", end="")
            while i < len(text):
                if b < i and i < e:
                    print(Fore.RED + str(i), end = "")
                else:
                    print(str(i), end = "")
                i+=1
                if i < len(text):
                    print(", ", end="")
            print("]")



    def iterateText(self, text):
        self.texts = [self.__concat_text(text)]
        self.paths_of_stats = [ [0] ]

        starting_status = status(self.mess["s0"][0], self.mess["s0"][1], 0)     # implicitly set to "st0" and 0 
        self.stats = [starting_status]
        self.size_of_window = self.mess["size_of_window"]                       # implicitly set to 1

        print(self.texts[0])
        while True:
            try:
                s = self.stats.pop()
                print(f"     > taking status : {s}")
                window = self.__get_window(self.texts[s.text_version], s.position)
                print(f" text: {self.texts[s.text_version]}")
                print(f" window: {window}")
                self.__move(window, s)
            except:
                if self.is_accepting_state(s.state):
                    print(f"remaining tuples = {self.stats}")
                    print(f"number of copies of text = {len(self.texts)}")
                    self.prety_print(s)
                    return True
                elif self.stats.__len__() == 0:
                    return False


    def print_instructions(self):
        for state in self.mess["instructions"]:
            print(f"states: {state}: <" , end="")
            for value in self.mess["instructions"][state]:
                print(f" \"{value}\" : [", end = "")
                for instruct in self.mess["instructions"][state][value]:
                    print(f"{instruct}", end = "")
                print("]", end ="")
            print(">")


    def save_instructions(self, to):
        with open(to, "w") as to_file:
            json.dump(self.mess, to_file)  


    def is_deterministic(self):
        for state in self.mess["instructions"]:
            for value in self.mess["instructions"][state]:
                if len(self.mess["instructions"][state][value]) > 1:
                    return False
        return True
    
    def clear(self):
        self.mess = {}
