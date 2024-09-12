from default_functions.statements import Statements
import globals
from walking_tools.organisers import Organisers
from walking_tools.dissectors import Dissectors
from default_functions.assigment import Assignment
from default_functions.functions import Functions
from default_functions.loops import Loops


statements = {
        "declare" : Assignment.var_declaration, 
        "assign" : Assignment.var_assignment, 
        "func" : Functions.function_declaration,
        "return" : Functions.return_val, 
        "del" : Functions.delete_var,
        "delete" : Functions.delete_var,
        "print" : Functions.print_function,
        "for" : Loops.for_loop,
        "while" : Loops.while_loop,
        "if" : Statements.if_statement,
        "elif" : Statements.elif_statement,
        "else" : Statements.else_statement,
}


def process_lines(lines : list, inside_function = ""):
    #print(f"processing lines inside_function {inside_function}")
    globals.inside_function = inside_function

    commentless_lines = []
    for line in lines:
        if not line.strip()[:2] == "//":
            commentless_lines.append(line)

    full_program = " ".join(commentless_lines)

    # clean out potential whitespace issues, etc.
    full_program = " ".join(full_program.split())
    error, program_commands = Dissectors.dissect_program(full_program) #full_program.split(";")
    command_index = 0
    skip_indexes = []



    for command in program_commands:

        command = command.strip()

        if command_index in skip_indexes:
            command_index += 1
            continue


        status, skips = run_command(command, command_index, program_commands)
        if status == 400:
            break
        skip_indexes += skips
        if len(skip_indexes) > 10:
            skip_indexes[:] = [x for x in skip_indexes if x > command_index]

        command_index += 1

def run_command(command, command_index, total_commands) -> tuple[int, list]:
    commands = command.strip().split(" ")
    found = False
    #print(f"running {command}")
    for statement in statements:
        if statement == command[:len(statement)]:
            #print("FOUND")
            command = command[:len(statement)]
            #print(f"command {command}")
            found = True
            skip, status = statements[command](commands, command_index, total_commands)
            #print(f"skips {skip}, status {status}")
            if status == 400:
                return 400, []
            else:
                return 200, skip

    if not found:
        if len(commands) >= 3 and commands[1] == ":":
            #print(f"sending commands: {commands}\nindex = {command_index}\ncommands = {program_commands}")
            skip, status = statements["declare"](commands, command_index, total_commands)

            if status == 400:
                return 400, []
            else:
                return 200, skip

        elif len(commands) >= 3 and commands[1] in ["=", "+=", "-="] and commands[0].isalnum(): # and len(command) == 3:
            skip, status = statements["assign"](commands, command_index, total_commands)

            if status == 400:
                return 400, []
            else:
                return 200, skip

    elif command.strip() not in ["{", "}", ";"] and not found:
        open_index = Organisers.find_first_char("(", command.strip()) + 1

        if commands[0].strip()[:open_index - 2] in globals.functions:
            pass
        else:
            print(f"Err - {command} is not a known function.")
            return 400, []


    return 200, []



