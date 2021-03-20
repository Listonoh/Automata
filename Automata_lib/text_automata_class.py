from Automata_lib import Automaton


class Text_Automaton(Automaton):
    def load_key(self, key, rest_of_line):
        if key in ["accepting_states", "alphabet"]:
            setattr(self, key, [i.strip() for i in rest_of_line.split(",")])
        elif key == "size_of_window":
            self.size_of_window = int(rest_of_line)
        else:
            setattr(self, key, rest_of_line)

    def load_line(self, line: str):
        parsed_line = line.split(":")
        key = parsed_line[0].strip()

        if key in self.definition.keys():
            rest_of_line = line[len(parsed_line[0]) + 1:].lstrip()
            self.load_key(key, rest_of_line)
        else:
            self.load_instruction(line)

    def load_instruction(self, line: str):
        first_part, second_part = line.split("->")
        from_state, window = first_part.strip().split()
        to_state, instruction = second_part.strip().split()
        self.add_instr(from_state, window, to_state, instruction)

    def load(self, file_name):
        with open(file_name, "r") as file:
            for line in file:
                self.load_line(line)

    def _stringify_instructions(self, value):
        for state, instructions in value.items():
            for window, possible_outcomes in instructions.items():
                for new_state, instruction in possible_outcomes:
                    sting_window = "".join(
                        item[1:-1] for item in window[1:-1].split(", ")
                    )
                    return "{} {} -> {} {}\n".format(
                        state, sting_window, new_state, instruction
                    )

    def _stringify_line_for_save(self, key, value) -> str:
        if key != "instructions":
            if type(value) is list:
                return "{}: {}".format(key, ", ".join(value))
            else:
                return "{}: {}".format(key, value)
        else:
            return self._stringify_instructions(value)

    def save(self, file):
        with open(file, "w") as out_file:
            for key, value in self.definition.items():
                out_file.write(self._stringify_line_for_save(key, value))
