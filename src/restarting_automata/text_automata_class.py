from .automata_class import BaseAutomaton, OutputMode


class Automaton(BaseAutomaton):
    def __init__(self, file="", out_mode=OutputMode.INSTRUCTIONS, output=False):
        self.out = out_mode
        self.output = output
        self.instructions = {}
        if file:
            try:
                self.load_text(file)
            except (FileNotFoundError):
                self.log(2, "\nAutomaton can not be loaded")
                print("file not found")

    def __load_key(self, key, rest_of_line):
        if key in ["alphabet", "working_alphabet"]:
            setattr(
                self,
                key,
                []
                if rest_of_line == ""
                else [i.strip() for i in rest_of_line.split(",")],
            )
        elif key == "size_of_window":
            self.size_of_window = int(rest_of_line)
        else:
            setattr(self, key, rest_of_line)

    def __load_instruction(self, line: str):
        first_part, right_side = line.split("->")
        from_state, window = first_part.strip().split()
        right_side = right_side.split()
        if len(right_side) == 1:
            self.add_instruction_without_state(from_state, window, right_side[0])
        elif len(right_side) == 2:
            self.add_instruction(from_state, window, right_side[0], right_side[1])

    def __load_line(self, line: str):
        line = line.replace("\n", "")
        parsed_line = line.split(":")
        key = parsed_line[0].strip()

        if key in self.definition.keys():
            # parsed line pherhaps
            rest_of_line = line[len(parsed_line[0]) + 1 :].lstrip()
            self.__load_key(key, rest_of_line)
        else:
            self.__load_instruction(line)

    def load_from_string(self, lines):
        for line in lines:
            self.__load_line(line)

    def load_text(self, file_name):
        with open(file_name, "r") as file:
            for line in file:
                self.__load_line(line)
            # self.load_from_string(file)

    def __stringify_instructions(self, value):
        return_value = []
        for state, instructions in value.items():
            for window, possible_outcomes in instructions.items():
                for right_side in possible_outcomes:
                    sting_window = "".join(
                        item[1:-1] for item in window[1:-1].split(", ")
                    )
                    if type(right_side) is list:
                        instruction = right_side[1]
                        if instruction not in self.special_instructions:
                            instruction = "".join(eval(right_side[1]))
                        return_value.append(
                            "{} {} -> {} {}".format(
                                state, sting_window, right_side[0], instruction
                            )
                        )
                    elif type(right_side) is str:
                        return_value.append(
                            "{} {} -> {}".format(state, sting_window, right_side)
                        )

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
                out_file.write(self.__stringify_line_for_save(key, value) + "\n")
            out_file.close()
