from Automata_lib import Automaton


class Text_Automaton(Automaton):
    def __load_key(self, key, rest_of_line):
        if key in ["accepting_states", "alphabet"]:
            setattr(self, key, [i.strip() for i in rest_of_line.split(",")])
        elif key == "size_of_window":
            self.size_of_window = int(rest_of_line)
        else:
            setattr(self, key, rest_of_line)

    def __load_instruction(self, line: str):
        first_part, second_part = line.split("->")
        from_state, window = first_part.strip().split()
        to_state, instruction = second_part.strip().split()
        self.add_instr(from_state, window, to_state, instruction)

    def __load_line(self, line: str):
        line = line.replace("\n", "")
        parsed_line = line.split(":")
        key = parsed_line[0].strip()

        if key in self.definition.keys():
            rest_of_line = line[len(parsed_line[0]) + 1:].lstrip()
            self.__load_key(key, rest_of_line)
        else:
            self.__load_instruction(line)

    def load_from_string(self, lines):
        for line in lines:
            self.__load_line(line)

    def load_text(self, file_name):
        with open(file_name, "r") as file:
            self.load_from_string(file)

    def __stringify_instructions(self, value):
        return_value = []
        for state, instructions in value.items():
            for window, possible_outcomes in instructions.items():
                for new_state, instruction in possible_outcomes:
                    sting_window = "".join(
                        item[1:-1] for item in window[1:-1].split(", ")
                    )
                    return_value.append("{} {} -> {} {}".format(
                        state, sting_window, new_state, instruction
                    ))
        return "\n".join(return_value)

    def __stringify_line_for_save(self, key, value) -> str:
        if key != "instructions":
            if type(value) is list:
                return "{}: {}".format(key, ", ".join(value))
            else:
                return "{}: {}".format(key, value)
        else:
            return self.__stringify_instructions(value)

    def save_text(self, file):
        self.alphabet = sorted(self.alphabet)
        with open(file, "w") as out_file:
            for key, value in self.definition.items():
                out_file.write(
                    self.__stringify_line_for_save(key, value) + "\n")
