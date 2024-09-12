
from walking_tools.organisers import Organisers
from evaluator import Evaluator
import globals

class Functions:

    @staticmethod
    def function_declaration(commands, command_index, program_commands) -> tuple[list, int]:
        #command = commands[command_index]
        command = " ".join(commands)
        skip_indexes = []

        nom_open_index = Organisers.find_first_char("(", commands[1].strip())
        open_index = Organisers.find_first_char("(", command.strip()) + 1
        close_index = Organisers.find_first_char(")", command.strip())
        final_bracket = Organisers.find_final_bracket(program_commands[command_index + 1:]) + 1

        globals.functions[commands[1][:nom_open_index]] = [[], []]

        func_vars = command.strip()[open_index:close_index].split(",")
        for var in func_vars:
            globals.functions[commands[1][:nom_open_index]][0].append(var.strip())

        for i in range((command_index + 1), (command_index + final_bracket)):
            globals.functions[commands[1][:nom_open_index]][1].append(program_commands[i])
            skip_indexes.append(i)

        return skip_indexes, 200

    @staticmethod
    def delete_var(commands, command_index, program_commands) -> tuple[list, int]:
        if not commands[1][:-1] in globals.variables:
            print(f"Err - unable to free unknown var '{commands[1][:-1]}'")
            return [], 400
        else:
            globals.variables.pop(commands[1][:-1])

        return [], 200

    @staticmethod
    def return_val(commands, command_index, program_commands) -> tuple[list, int]:
        #command = commands[command_index]
        command = " ".join(commands)
        print(f"command = {command} and inside_function {globals.inside_function}")
        if globals.inside_function:
            globals.variables["$#" + globals.inside_function] = Evaluator.evaluate_expression(command.strip()[7:].strip())

        else:
            print(f"Err - orphaned return.")
            return [], 400

        return [], 200

    @staticmethod
    def print_function(commands, command_index, program_commands) -> tuple[list, int]:
        #command = commands[command_index]
        command = " ".join(commands)

        text = Evaluator.evaluate_expression(command.strip()[6:-2], bracketted = True)
        print(f"{text}")

        return [], 200

