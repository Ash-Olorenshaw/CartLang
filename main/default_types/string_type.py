

class StringType:
    @staticmethod
    def evaluate_string_func(func_name : str, arguments : list):
        match func_name:
            case "to_string":
                if len(arguments) > 1:
                    print(f"Err - string.to_string() expected 1 argument, received {len(arguments)}")
                return str(arguments[0])
