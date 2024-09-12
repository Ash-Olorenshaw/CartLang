
class FloatType:
    @staticmethod
    def evaluate_float_func(func_name : str, arguments : list):
        match func_name:
            case "to_float":
                if len(arguments) > 1:
                    print(f"Err - float.to_float() expected 1 argument, received {len(arguments)}")
                return float(arguments[0])

