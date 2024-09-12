import start_message
import line_reader
import globals

def run(file : str, debug : bool = False):
    with open(file, "r+", encoding="utf-8") as output_file:
        programlines = output_file.readlines()

    if debug:
        print(start_message.message)

    line_reader.process_lines(programlines)

    if debug:
        print(f"INTERPRETER OUT: final vars = {globals.variables}")
        print(f"INTERPRETER OUT: final funcs = {globals.functions}")
