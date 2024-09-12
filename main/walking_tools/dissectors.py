
class Dissectors:
    @staticmethod
    def dissect_program(full_program : str):
        char_index = 0
        current_line = ""
        dissected_program = []

        for char in full_program:
            current_line += char
            if char in [";", "{", "}"]:
                dissected_program.append(current_line)
                current_line = ""
            elif char == "\n":
                # this is never called as there should never be newlines.
                #print("ENCOUNTERED NEWLINE")
                dissected_program.append(current_line)
                current_line = ""
            char_index += 1

        if dissected_program != []:
            return 200, dissected_program
        else:
            return 400, dissected_program


