from evaluator import Evaluator

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
    
    @staticmethod
    def create_variables(var_string : str):
        temp_func_vars = var_string.split(",")
        func_vars = []
        inside_item = False

        temp_var = ""
        for var in temp_func_vars:
            var = var.strip()
            print(f"processing {var}")
            if var[0] in ['"', "["] and not inside_item:
                inside_item = True
                temp_var += var + ", "
            elif var[-1] in ['"', "]"] and inside_item:
                inside_item = False
                temp_var += var
            elif inside_item:
                temp_var += var + ", "

            if not inside_item:
                if temp_var == "":
                    print(f"appending {var}")
                    func_vars.append(Evaluator.evaluate_expression(var, bracketted = True, var_names = True))
                else:
                    print(f"appending {temp_var}")
                    func_vars.append(Evaluator.evaluate_expression(temp_var, bracketted = True, var_names = True))

                temp_var = ""

        return func_vars





