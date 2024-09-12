

class IntType:
    @staticmethod
    def evaluate_int_func(func_name : str, arguments : list):
        match func_name:
            case "to_int":
                if len(arguments) > 1:
                    print(f"Err - int.to_int() expected 1 argument, received {len(arguments)}")
                return int(arguments[0])
