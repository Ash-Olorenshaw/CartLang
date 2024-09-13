from walking_tools.organisers import Organisers
from evaluator import Evaluator
from collections.abc import Iterable
import globals
import line_reader



class Loops:

    @staticmethod
    def for_loop(commands, command_index, program_commands) -> tuple[list, int]:
        skip_indexes = []
        #command = commands[command_index]
        command = " ".join(commands)

        if commands[2] != "in" and commands[2] != "->":# in command.strip():
            print(f"Err - malformed line {command.strip()}. Unable to find 'in' or '->' in 'for' loop.")
            return skip_indexes, 400
        
        globals.variables[commands[1][1:]] = None

        open_index = Organisers.find_first_char("(", command.strip()) + 1 + len(commands[1]) + len(commands[2]) + 1
        close_index = Organisers.find_first_char(")", command.strip())
        iteration_item = Evaluator.evaluate_expression(command.strip()[open_index:close_index], bracketted = True)

        if type(iteration_item) == int:
            iteration_item = range(iteration_item)

        if isinstance(iteration_item, Iterable):
            final_bracket = Organisers.find_final_bracket(program_commands[command_index + 1:]) + 1

            for i in range((command_index + 1), (command_index + final_bracket)):
                skip_indexes.append(i)

            for val in iteration_item:
                globals.variables[commands[1][1:]] = val
                line_reader.process_lines(program_commands[command_index + 1:command_index + final_bracket])

            return skip_indexes, 200
        else:
            print(f"Err - {iteration_item} is not iterable for 'for' loop.")
            return skip_indexes, 400

    @staticmethod
    def while_loop(commands, command_index, program_commands) -> tuple[list, int]:
        skip_indexes = []
        #command = commands[command_index]
        command = " ".join(commands)
        open_index = Organisers.find_first_char("(", command.strip()) + 1
        close_index = Organisers.find_first_char(")", command.strip())
        statement = Evaluator.evaluate_expression(command.strip()[open_index:close_index], bracketted = True)

        if isinstance(statement, bool):
            final_bracket = Organisers.find_final_bracket(program_commands[command_index + 1:]) + 1

            for i in range((command_index + 1), (command_index + final_bracket)):
                skip_indexes.append(i)

            while statement:
                line_reader.process_lines(program_commands[command_index + 1:command_index + final_bracket])
                statement = Evaluator.evaluate_expression(command.strip()[open_index:close_index], bracketted = True)

            return skip_indexes, 200

        else:
            print(f"Err - {statement} is not type 'bool' - not compatible with 'while' loop.")
            return skip_indexes, 400

    




