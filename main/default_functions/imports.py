import os
import main
import globals
from evaluator import Evaluator
from type_conversions import Types

class Imports:
    @staticmethod
    def import_file(commands, command_index, program_commands) -> tuple[list, int]:
        if len(commands) > 2:
            print("Err - too many args for 'open' - please only pass one string.")
            return [], 400

        if commands[1][-1] == ";":
            pth = commands[1][:-1]
        else:
            pth = commands[1]

        import_path = Types.convert_to_correct_type(pth)
        if type(import_path) == str:
            current_path = globals.working_dir
            path_parts = import_path.split("/")
            for part in path_parts:
                if os.path.exists(os.path.dirname(current_path + "/" + part)):
                    current_path += "/" + part
                else:
                    print(f"Err - path does not exist '{current_path + '/' + part}'")
                    return [], 400

            prev_dir = globals.working_dir
            main.run(current_path, debug = False)
            globals.working_dir = prev_dir

            return [], 200
        else:
            print(f"Err - type '{type(import_path)}' of import path '{import_path}' is not compatible - expected type 'str'")
            return [], 400



