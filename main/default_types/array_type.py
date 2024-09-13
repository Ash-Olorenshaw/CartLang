import globals

class ArrayType:
    @staticmethod
    def evaluate_array_func(func_name : str, arguments : list):
        match func_name:
            case "append":
                if 2 > len(arguments) > 2:
                    print(f"Err - array.append() expected 2 arguments, received {len(arguments)}")
                print(f"var {arguments[0]} to append {arguments[1]}")
                globals.variables[arguments[0]].append(arguments[1])
                return globals.variables[arguments[0]]
