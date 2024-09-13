from evaluator import Evaluator
import globals

class Assignment:

    @staticmethod
    def var_declaration(commands, command_index, program_commands) -> tuple[list, int]:
        skip_indexes = []
        command = " ".join(commands)

        if commands[0] not in globals.variables:
            globals.variables[commands[0]] = None
            leftItem = commands[0]
            command_right_side = command.split("=")[1].strip()#[:-1]
            rightItem = Evaluator.evaluate_expression(command_right_side)

            match commands[2]:
                case "int":
                    if type(rightItem) != int:
                        print(f"Err - type int does not match '{rightItem}'")
                        return skip_indexes, 400
                case "string":
                    if type(rightItem) != str:
                        print(f"Err - type string does not match '{rightItem}'")
                        return skip_indexes, 400
                case "float":
                    if type(rightItem) != float:
                        print(f"Err - type float does not match '{rightItem}'")
                        return skip_indexes, 400
                case "bool":
                    if type(rightItem) != bool:
                        print(f"Err - type bool does not match '{rightItem}'")
                        return skip_indexes, 400
                case _:
                    print(f"Err - type '{commands[2]}' is unknown")
                    return skip_indexes, 400

            globals.variables[leftItem] = rightItem
            return skip_indexes, 200

        else:
            print(f"Err - attempting to create already existing var {commands[0]}")
            return skip_indexes, 400

    @staticmethod
    def var_assignment(commands, command_index, program_commands) -> tuple[list, int]:
        skip_indexes = []
        #command = commands[command_index]
        command = " ".join(commands)
        assigner = commands[1]
        #print(f"entered assignment on {command}")
        leftItem = None
        rightItem = None
        if commands[0] in globals.variables:
            leftItem = commands[0]

        else:
            print(f"Err - Unable to perform operation {assigner} on nonexistant var {commands[0]}")
            return skip_indexes, 400

        command_right_side = command.split(assigner)[1].strip()#[:-1]
        rightItem = Evaluator.evaluate_expression(command_right_side)

        if type(globals.variables[leftItem]) != type(rightItem) and globals.variables[leftItem] != None:
            print(f"Err - {leftItem}({globals.variables[leftItem]})'s type {type(globals.variables[leftItem])} doesn't match {type(rightItem)}")
            return skip_indexes, 400


        if assigner == "=":
            globals.variables[leftItem] = rightItem
        elif assigner == "+=":
            if type(rightItem) in [str, int, float]:
                globals.variables[leftItem] += rightItem
            else:
                print(f"Err - Unable to perform operation {assigner} on type {type(rightItem)}")
                return skip_indexes, 400
        elif assigner == "-=":
            if type(rightItem) in [int, float]:
                globals.variables[leftItem] -= rightItem
            elif type(rightItem) == str:
                var_val = globals.variables[leftItem]
                if var_val[:len(var_val)] == rightItem:
                    globals.variables[leftItem] = var_val[len(rightItem):]
                elif var_val[len(var_val):] == rightItem:
                    globals.variables[leftItem] = var_val[:len(rightItem)]
                else:
                    print(f"Err - unable to perform string deletion operation. String '{var_val}' does not contain '{rightItem}'")
                    return skip_indexes, 400

            else:
                print(f"Err - Unable to perform operation {assigner} on type {type(rightItem)}")
                return skip_indexes, 400

        return skip_indexes, 200




