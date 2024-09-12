
class Organisers:
    @staticmethod
    def find_final_bracket(lines : list, bracket : str = "{"):
        #find_final_cbracket
        # int that stores how many brackets have been opened.
        brackets = 1
        if bracket == "(":
            alt_bracket = ")"
        elif bracket == "[":
            alt_bracket = "]"
        elif bracket == "<":
            alt_bracket = ">"
        else:
            alt_bracket = "}"
        line_int = 0
        char_int = 0

        for line in lines:
            char_int = 0
            for char in line:
                if char == alt_bracket:
                    #print(f"found alt {char} in {line}")
                    brackets -= 1
                elif char == bracket:
                    #print(f"found {char} in {line}")
                    brackets += 1

                if brackets == 0:
                    #print("break 1")
                    break

                char_int += 1

            if brackets == 0:
                #print("break 1")
                break

            line_int += 1

        
        if line_int == 0:
            #print(f"char_int = {char_int}")
            return char_int
        else:
            #print(f"line_int = {line_int}")
            return line_int

    @staticmethod
    def split_organise(expressions : str, orphaned : bool = False) -> list:
        """
        Splits up the given string into separate expressions while also respecting strings.
        | `expressions` (str) - the string of the expressions to be split and processed.
        """
        #print(f"split organisaing {expressions}")
        prev_char_whitespace = False
        split_start = 0
        split_end = 0
        inside_string = False
        char_index = 0
        split_expressions = []
        for char in expressions:
            if char.isspace() and not prev_char_whitespace and not inside_string:
                #print(f"{char} option 1")
                prev_char_whitespace = True
                split_end = char_index 
                if len(expressions) > char_index + 1 and not expressions[char_index + 1].isspace():
                    split_expressions.append(expressions[split_start:split_end])
                    split_start = char_index + 1
            elif char_index == len(expressions) - 1 and char == ";":
                #print(f"{char} colonSplit")
                prev_char_whitespace = True
                split_end = char_index 
                split_expressions.append(expressions[split_start:split_end])#[:-1])
            elif char_index == len(expressions) - 1 and orphaned:
                #print(f"{char} orphanedSplit")
                prev_char_whitespace = True
                split_end = char_index + 1
                split_expressions.append(expressions[split_start:split_end])#[:-1])
            elif char == '"' and not inside_string:
                #print(f"{char} option 4")
                inside_string = True
                split_start = char_index
            elif char == '"' and inside_string:
                #print(f"{char} option 5")
                inside_string = False 
                split_end = char_index - 1
            elif not char.isspace() and prev_char_whitespace:
                #print(f"{char} option skip")
                prev_char_whitespace = False
            #else:
            #    print(f"{char} else!")
            #else:
                #print(f"no operation performed on char {char} with prev_char_whitespace {prev_char_whitespace} and inside_string {inside_string}")
            char_index += 1

        #print(f"finalised split_expressions: {split_expressions}")
        return split_expressions

    @staticmethod
    def find_first_char(char : str, total : str):

        found = False
        char_index = 0
        for c in total:
            if c == char:
                found = True
                break
            char_index += 1

        if not found:
            print(f"Err - malformed line. Unable to find {char} in {total}.")
        return char_index


