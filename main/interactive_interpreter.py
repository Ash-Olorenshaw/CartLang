import globals
import start_message
import line_reader
from walking_tools.dissectors import Dissectors

def interactive_interpret():

    print(start_message.message)
    print("Interactive terminal mode.")

    line = ""
    quit_interactive = False
    while True:
        temp_line = input(" ")
        if temp_line.strip() in ["exit", "quit", "end", "quit()", "exit()", "exit();"]:
            print("Err - line ignored. Did you mean 'quit();'?")
            continue
        elif temp_line.strip() in ["clear()", "clear();"]:
            print("Clearing command history...")
            line = ""
            continue
        line += temp_line
        

        # clean out potential whitespace issues, etc.
        full_program = " ".join(line.split())

        error, program_commands = Dissectors.dissect_program(full_program) #full_program.split(";")
        if error == 200:
            line = ""
            command_index = 0
            skip_indexes = []


            for command in program_commands:
                command = command.strip()
                if command[:2] == "//":
                    continue
                elif command_index in skip_indexes:
                    command_index += 1
                    continue
                elif command == "quit();":
                    quit_interactive = True
                    break

                status, skips = line_reader.run_command(command, command_index, program_commands)
                if status == 400:
                    break
                skip_indexes += skips
                if len(skip_indexes) > 10:
                    skip_indexes[:] = [x for x in skip_indexes if x > command_index]

                command_index += 1

            if quit_interactive:
                break

    print(f"INTERPRETER OUT: final vars = {globals.variables}")
    print(f"INTERPRETER OUT: final funcs = {globals.functions}")
    print("done!")
