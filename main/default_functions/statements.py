from walking_tools.organisers import Organisers
from evaluator import Evaluator
import globals


class Statements:
    """
    Every func returns: 
    - `skip_indexes`
    - `status_code`
    """

    @staticmethod
    def if_statement(commands, command_index, program_commands) -> tuple[list, int]:
        #command = commands[command_index]
        command = " ".join(commands)
        skip_indexes = []

        skip_indexes = []
        open_index = Organisers.find_first_char("(", command.strip()) + 1
        close_index = Organisers.find_first_char(")", command.strip())
        #print(f"found open index as {open_index} and close as {close_index}")

        statement = Evaluator.evaluate_expression(command.strip()[open_index:close_index], bracketted = True)
        final_bracket = Organisers.find_final_bracket(program_commands[command_index + 1:]) + 1
        if statement:
            #program_commands.pop(command_index + final_bracket)
            skip_indexes.append(command_index + final_bracket)
            globals.previous_if = 1
            #print(f"popping {final_bracket}")
            
            #print(f"True for {command}")
        else:
            for i in range((command_index + 1), (command_index + final_bracket)):
                skip_indexes.append(i)
            globals.previous_if = 0
            #print(f"False for {command}")

        return skip_indexes, 200

    @staticmethod
    def elif_statement(commands, command_index, program_commands) -> tuple[list, int]:
        #command = commands[command_index]
        command = " ".join(commands)
        skip_indexes = []

        open_index = Organisers.find_first_char("(", command.strip()) + 1
        close_index = Organisers.find_first_char(")", command.strip())

        if globals.previous_if == -1:
            print(f"Err - orphaned elif statement.")
            return skip_indexes, 400


        statement = Evaluator.evaluate_expression(command.strip()[open_index:close_index], bracketted = True)
        final_bracket = Organisers.find_final_bracket(program_commands[command_index + 1:]) + 1

        if statement and globals.previous_if == 0:
            skip_indexes.append(command_index + final_bracket)
            globals.previous_if = 1
        else:
            for i in range((command_index + 1), (command_index + final_bracket)):
                skip_indexes.append(i)

        return skip_indexes, 200

    @staticmethod
    def else_statement(commands, command_index, program_commands) -> tuple[list, int]:
        skip_indexes = []

        if globals.previous_if == -1:
            print(f"Err - orphaned else statement.")
            return skip_indexes, 400

        final_bracket = Organisers.find_final_bracket(program_commands[command_index + 1:]) + 1

        if globals.previous_if == 0:
            skip_indexes.append(command_index + final_bracket)
        else:
            for i in range((command_index + 1), (command_index + final_bracket)):
                skip_indexes.append(i)

        globals.previous_if = -1
        return skip_indexes, 200




