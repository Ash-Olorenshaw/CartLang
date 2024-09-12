"""
NOTICE!!

This is a backup of the original interpreter which was all in a single file.
This file is no longer used since the rest of the project has since moved on, but this is kept for posterity.

"""


import start_message
from default_types.string_type import StringType
from default_types.int_type import IntType
from collections.abc import Iterable

programlines = []
variables = {}
functions = {"gamma" : []}

with open("test.cart", "r+", encoding="utf-8") as output_file:
    programlines = output_file.readlines()

def is_comparison_operator(op : str):
    if op in ["&&", "||", "==", "!=", ">=", "<=", ">", "<"] or "~" in op:
        return True
    else:
        return False
    

def collate_strings(items : list):
    collated_items = []
    stringing = False
    string_pos = 0
    for item in items:
        #print(f"processing item {item}")
        if item == '"':
            #print('" encountered')
            if not stringing:
                string_pos = items.index(item)
                stringing = True
                collated_items.append(item)
            else:
                collated_items[string_pos] += item
                stringing = False
                string_pos = 0
        elif stringing:
            #print('stringing')
            collated_items[string_pos] += item
        else:
            #print('basic appended')
            collated_items.append(item)

    return collated_items

def check_next_item(item : str):
    """
    returns True if the item supplied doesn't exist.
    """
    try:
        if item not in ["+", "-", "&&", "*", "/", "%", ":", "||", "==", "!=", ">=", "<=", ">", "<"] and "~" not in item:
            next_expression = convert_to_correct_type(item)
            if next_expression == None:
                return True
    except:
        pass

    return False

def convert_to_correct_type(item : str):
    val = None
    item = item.strip()

    if "." in item:
        try: val = float(item)
        except: pass
    elif item in variables:
        val = variables[item]
    elif item.isdigit():
        val = int(item)
    elif item[0] == '"' and item[-1] == '"':
        val = str(item[1:-1])


    return val

def find_final_cbracket(lines : list):
    # int that stores how many brackets have been opened.
    brackets = 1
    line_int = 0

    for line in lines:
        if line.strip() == "}":
            brackets -= 1
        if line.strip() == "{":
            brackets += 1


        if brackets == 0:
            break

        line_int += 1

    return line_int

def perform_comparison(item1 : str, comparator : str, item2 : str):
    return_val = False

    if type(item1) == str:
        first_item = convert_to_correct_type(item1)
    else:
        first_item = item1
    if type(item2) == str:
        second_item = convert_to_correct_type(item2)
    else:
        second_item = item2


    if comparator == "==":
        return_val = (second_item == first_item)
    elif comparator == "!=":
        return_val = (second_item != item1)
    elif comparator == ">":
        if type(first_item) in [int, float]:
            return_val = (second_item < first_item)
        else:
            return_val = (len(second_item) < len(first_item))
    elif comparator == "<":
        if type(first_item) in [int, float]:
            return_val = (second_item > first_item)
        else:
            return_val = (len(second_item) > len(first_item))
    elif comparator == "<=":
        if type(first_item) in [int, float]:
            return_val = (second_item >= first_item)
        else:
            return_val = (len(second_item) >= len(first_item))
    elif comparator == ">=":
        if type(first_item) in [int, float]:
            return_val = (second_item <= first_item)
        else:
            return_val = (len(second_item) <= len(first_item))
    elif "~" in comparator:
        width = comparator.strip()[1:]
        if "-" in width:
            print(f"Err - circa operator cannot be used with negative integers ({item1} {comparator} {item2}).")
        elif width.isdigit():
            return_val = (first_item <= second_item + int(width) and first_item >= second_item - int(width))
            #print(f"returnval set to {return_val}")
        else:
            print(f"Err - circa operator cannot be used with non-digit '{comparator}' ({item1} {comparator} {item2}).")
    elif comparator in ["||", "&&"] or not comparator:
        return_val = True
    else:
        print(f"Err - unrecognised string comparison '{str(first_item) + comparator + str(second_item)}'")
        return -1

    if return_val:
        return 1
    else:
        return 0


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
            if not expressions[char_index + 1].isspace():
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


def evaluate_expression(expression : str, bracketted = False):
    #expressions = expression.split(" ")
    #expressions = collate_strings(expressions)
    if not bracketted:
        expressions = split_organise(expression)
    else:
        expressions = split_organise(expression, orphaned = True)

    #print(f"split expressions = {expressions}")

    rightItem = None
    found_full_expression = False
    last_operator = ""
    multi_store = None
    last_operators = []
    exp_index = 0

    #print(f"expression: {expressions}")
    if "||" in expressions or "&&" in expressions:
        #print(f"multi_store set to []")
        multi_store = []

    for exp in expressions:
        #print(f"processings {exp}")
        if found_full_expression:
            print(f"Err - expression is not comprehendable - contains too many arguments.")
            break

        if exp not in ["+", "-", "&&", "*", "/", "%", ":", "||", "==", "!=", ">=", "<=", ">", "<"] and not "~" in exp and multi_store == None:
            try:
                found_full_expression = check_next_item(expressions[exp_index + 1])
            except IndexError as e:
                pass
            is_float = False
            if "." in exp:
                try: 
                    float(exp)
                    is_float = True
                except: 
                    is_float = False

            if "." in exp and not is_float:
                dec_split_items = exp.split(".")

                open_index = find_first_char("(", dec_split_items[1].strip()) + 1
                close_index = find_first_char(")", dec_split_items[1].strip())

                temp_func_vars = dec_split_items[1].strip()[open_index:close_index].split(",")
                func_vars = []

                for var in temp_func_vars:
                    func_vars.append(evaluate_expression(var, bracketted = True))

                func_name = dec_split_items[1].strip()[:open_index - 1]

                if dec_split_items[0] == "string":
                    func_return = StringType.evaluate_string_func(func_name, func_vars)
                    if last_operator == "":
                        rightItem = func_return



                elif dec_split_items[0] == "int":
                    func_return = IntType.evaluate_int_func(func_name, func_vars)
                    if last_operator == "":
                        rightItem = func_return


            elif exp in variables:
                val = variables[exp]

                if last_operator == "":
                    rightItem = val

                elif type(rightItem) == int and type(val) == int:
                    if last_operator == "+":
                        rightItem += val
                    elif last_operator == "-":
                        rightItem -= val
                    elif last_operator == "*":
                        rightItem = rightItem * val
                    elif last_operator == "/":
                        rightItem = rightItem / val
                    elif is_comparison_operator(last_operator):
                        pass

                    else:
                        print(f"Err - unsupported operation ({last_operator}) for int {exp}")
                        break

                elif type(rightItem) == float and type(val) == float:
                    if last_operator == "+" and type(val) == float:
                        rightItem += val
                    elif last_operator == "-":
                        rightItem -= val
                    elif last_operator == "*":
                        rightItem = rightItem * val
                    elif last_operator == "/":
                        rightItem = rightItem / val
                    elif is_comparison_operator(last_operator):
                        pass


                    else:
                        print(f"Err - unsupported operation ({last_operator}) for float {exp}")
                        break

                elif type(rightItem) == str and type(val) == str:
                    if last_operator == "+":
                        rightItem = rightItem + val
                    if last_operator == "-":
                        if rightItem[:len(val)] == val:
                            rightItem = rightItem[len(val):]
                        elif rightItem[len(val):] == val:
                            rightItem = rightItem[:len(val)]
                    elif is_comparison_operator(last_operator):
                        pass


                
                else:
                    print(f"Err - unsupported operation ({last_operator}) between {type(rightItem)} ({rightItem}) and {type(val)} ({val})")

                if not type(val) in [int, str, float]:
                    found_full_expression = True
            elif exp == "true":
                #if multi_store == None:
                rightItem = True
                #found_full_expression = True
                #else:
                #    multi_store.append(True)
            elif exp == "false":
                #if multi_store != None:
                #    multi_store.append(False)
                #else:
                rightItem = False
                #found_full_expression = True
            elif exp.isdigit():
                #if multi_store != None:
                #    multi_store.append(True)
                if last_operator == "":
                    rightItem = int(exp)
                else:
                    if type(rightItem) == int:
                        if last_operator == "+":
                            rightItem += int(exp)
                        elif last_operator == "-":
                            rightItem -= int(exp)
                        elif last_operator == "*":
                            rightItem = rightItem * int(exp)
                        elif last_operator == "/":
                            rightItem = rightItem / int(exp)
                        elif is_comparison_operator(last_operator):
                            pass


                        else:
                            print(f"Err - unsupported operation for int '{last_operator}'")
                            break

                        last_operator = ""
                    else:
                        print(f"Err - type {type(rightItem)} ({rightItem}) is not compatible with type int")
                        break
            elif is_float:
                if last_operator == "":
                    rightItem = float(exp)
                else:
                    if type(rightItem) == float:
                        if last_operator == "+":
                            rightItem += float(exp)
                        elif last_operator == "-":
                            rightItem -= float(exp)
                        elif last_operator == "*":
                            rightItem = rightItem * float(exp)
                        elif last_operator == "/":
                            rightItem = rightItem / float(exp)
                        elif is_comparison_operator(last_operator):
                            pass
                        else:
                            print(f"Err - unsupported operation for float '{last_operator}'")
                            break

                        last_operator = ""
                    else:
                        print(f"Err - type {type(rightItem)} ({rightItem}) is not compatible with type float")
                        break

            elif exp[0] == '"' and exp[-1] == '"':
                if last_operator == "":
                    rightItem = str(exp.strip('"'))
                else:
                    if last_operator == "+":
                        rightItem = rightItem + str(exp.strip('"'))
                    elif last_operator == "-":
                        strip_exp = str(exp.strip('"'))
                        if rightItem[:len(strip_exp)] == strip_exp:
                            rightItem = rightItem[len(strip_exp):]
                        elif rightItem[len(strip_exp):] == strip_exp:
                            rightItem = rightItem[:len(strip_exp)]
                        else:
                            print(f"Err - unable to perform string deletion operation. String '{rightItem}' does not contain '{strip_exp}'")
                    elif is_comparison_operator(last_operator):
                        pass


                    else:
                        print(f"Err - unsupported operation for string '{last_operator}'")
                        break
            else:

                open_index = find_first_char("(", exp.strip()) + 1

                #print(f"checking {exp.strip()[:open_index - 2]} against functions")
                if exp.strip()[:open_index - 2] in functions:
                    function = []
                    var_defaults = functions[exp.strip()[:open_index - 2]][0]
                    for var_default in var_defaults:
                        if "=" in var_default:
                            function.append(var_default + ";")

                    close_index = find_first_char(")", exp.strip())
                    func_vars = exp.strip()[open_index:close_index].split(",")
                    var_num = 0
                    for func_var in func_vars:
                        function.append(var_defaults[var_num] + " = " + func_var.strip() + ";")
                        var_num += 1

                    function = function + functions[exp.strip()[:open_index - 2]][1]
                    #print(f"processing lines:\n{function}")
                    process_lines(function, exp.strip()[:open_index - 2])
                    if last_operator == "":
                        rightItem = variables["$#" + exp.strip()[:open_index - 2]]

                else:
                    print(f"Err - expression {exp} is not comprehendable")
                    break
        else:
            #print(f"encountered exp {exp}")
            if not found_full_expression:
                #print(f"multi_store = {multi_store}")
                if multi_store == None:
                    if exp in ["==", "!=", ">=", "<=", ">", "<"] or "~" in exp:
                        try:
                            compare = perform_comparison(expressions[exp_index - 1], exp, expressions[exp_index + 1])
                            if compare == 0:
                                multi_store = [False]
                            elif compare == 1:
                                multi_store = [True]
                        except:
                            pass
                    else:
                        last_operator = exp
                else:
                    if exp in ["||", "&&"]:
                        try:
                            if expressions[exp_index + 2] in ["||", "&&"]:
                                next_expression = convert_to_correct_type(expressions[exp_index + 1])
                                if next_expression:
                                    multi_store.append(True)
                                else:
                                    multi_store.append(False)
                        except:
                            pass
                        last_operators.append(exp)
                    elif exp in ["==", "!=", ">=", "<=", ">", "<"] or "~" in exp:
                        #print(f"performing comparison {expressions[exp_index - 1] + exp + expressions[exp_index + 1]}")
                        compare = perform_comparison(expressions[exp_index - 1], exp, expressions[exp_index + 1])
                        #print(f"comparison resulted in {compare}")

                        if compare == -1:
                            comparitive_expression = " ".join(expressions[(exp_index-2):exp])
                            print(f"Err - unrecognised string comparison '{comparitive_expression}'")
                            break
                        else:
                            if compare == 0:
                                multi_store.append(False)
                            elif compare == 1:
                                multi_store.append(True)

            else:
                print(f"Err - orphaned operator. Current item = {rightItem}")
                break
        exp_index += 1

    if multi_store != None and multi_store != []:
        #print(f"current multi_store == {multi_store}")
        current_state = multi_store[0]
        for bool_val in range(len(multi_store)):
            #current_state = multi_store[bool_val]
            try:
                if last_operators[bool_val] == "&&":
                    if current_state and multi_store[bool_val + 1]:
                        current_state = True
                    else:
                        current_state = False
                elif last_operators[bool_val] == "||":
                    if (current_state == True) or (multi_store[bool_val + 1] == True):
                        current_state = True
                    else:
                        current_state = False
            except:
                pass
                #print("skip")

        rightItem = current_state


    return rightItem

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

def dissect_program(full_program : str):
    char_index = 0
    current_line = ""
    dissected_program = []

    for char in full_program:
        current_line += char
        if char in [";", "{", "}"]:
            dissected_program.append(current_line)
            current_line = ""
        elif char == "\n":
            print("ENCOUNTERED NEWLINE")
            dissected_program.append(current_line)
            current_line = ""
        char_index += 1

    return dissected_program


def process_lines(lines : list, inside_function = ""):
    commentless_lines = []
    for line in lines:
        if not line.strip()[:2] == "//":
            commentless_lines.append(line)

    full_program = " ".join(commentless_lines)

    #clean out potential whitespace issues, etc.
    full_program = " ".join(full_program.split())
    program_commands = dissect_program(full_program) #full_program.split(";")
    command_index = 0
    skip_indexes = []
    previous_if = -1

    for command in program_commands:
        #print(f"processing command {command}")
        #command = command + ";"
        ignore_indents = True
        #indentation_level = ""
        #if line[:len(indentation_level)] != indentation_level:
        #    print(f"Err - indentation level at line {lines.index(line)} is mismatched.")
        #    break
        #elif not line.isspace() and line.strip()[-1] != ";":
        #    print(f"Err - missing ; at line {lines.index(line)}. Given char {line[-1]} instead.")
        #    break
        if command_index not in skip_indexes:
            commands = command.strip().split(" ")
            #print(f"processing command {command.strip()[:5]}")
            if len(commands) >= 3 and commands[1] == ":":
                if commands[0] not in variables:
                    variables[commands[0]] = None
                    leftItem = commands[0]
                    command_right_side = command.split("=")[1].strip()#[:-1]
                    rightItem = evaluate_expression(command_right_side)

                    match commands[2]:
                        case "int":
                            if type(rightItem) != int:
                                print(f"Err - type int does not match '{rightItem}'")
                                break
                        case "string":
                            if type(rightItem) != str:
                                print(f"Err - type string does not match '{rightItem}'")
                                break
                        case "float":
                            if type(rightItem) != float:
                                print(f"Err - type float does not match '{rightItem}'")
                                break
                        case "bool":
                            if type(rightItem) != bool:
                                print(f"Err - type bool does not match '{rightItem}'")
                                break
                        case _:
                            print(f"Err - type '{commands[2]}' is unknown")
                            break

                    variables[leftItem] = rightItem

                else:
                    print(f"Err - attempting to create already existing var {commands[0]}")
            elif len(commands) >= 3 and commands[1] in ["=", "+=", "-="] and commands[0].isalnum(): # and len(command) == 3:
                assigner = commands[1]
                #print(f"entered assignment on {command}")
                leftItem = None
                rightItem = None
                if commands[0] in variables:
                    leftItem = commands[0]

                else:
                    print(f"Err - Unable to perform operation {assigner} on nonexistant var {commands[0]}")
                    break

                command_right_side = command.split(assigner)[1].strip()#[:-1]
                rightItem = evaluate_expression(command_right_side)

                if type(variables[leftItem]) != type(rightItem) and variables[leftItem] != None:
                    print(f"Err - {leftItem}({variables[leftItem]})'s type {type(variables[leftItem])} doesn't match {type(rightItem)}")
                    break

                if assigner == "=":
                    variables[leftItem] = rightItem
                elif assigner == "+=":
                    if type(rightItem) in [str, int, float]:
                        variables[leftItem] += rightItem
                    else:
                        print(f"Err - Unable to perform operation {assigner} on type {type(rightItem)}")
                        break
                elif assigner == "-=":
                    if type(rightItem) in [int, float]:
                        variables[leftItem] -= rightItem
                    elif type(rightItem) == str:
                        var_val = variables[leftItem]
                        if var_val[:len(var_val)] == rightItem:
                            variables[leftItem] = var_val[len(rightItem):]
                        elif var_val[len(var_val):] == rightItem:
                            variables[leftItem] = var_val[:len(rightItem)]
                        else:
                            print(f"Err - unable to perform string deletion operation. String '{var_val}' does not contain '{rightItem}'")

                    else:
                        print(f"Err - Unable to perform operation {assigner} on type {type(rightItem)}")
                        break                #print(f"setting var '{leftItem}' to '{rightItem}'")

            elif command.strip()[:5] == "print":
                #print(f"evaling {command.strip()[6:-2]}")
                #print(f"PRINTING!!")
                text = evaluate_expression(command.strip()[6:-2], bracketted = True)
                #print(f"printing text as {text}")
                print(f"{text}")

            elif command.strip()[:3] == "del" or command.strip()[:6] == "delete":
                if not commands[1][:-1] in variables:
                    print(f"Err - unable to free unknown var '{commands[1][:-1]}'")
                    break
                else:
                    variables.pop(commands[1][:-1])

            elif command.strip()[:2] == "if":
                skip_indexes = []
                open_index = find_first_char("(", command.strip()) + 1
                close_index = find_first_char(")", command.strip())
                #print(f"found open index as {open_index} and close as {close_index}")

                statement = evaluate_expression(command.strip()[open_index:close_index], bracketted = True)
                final_bracket = find_final_cbracket(program_commands[command_index:])
                if statement:
                    #program_commands.pop(command_index + final_bracket)
                    skip_indexes.append(command_index + final_bracket)
                    previous_if = 1
                    #print(f"popping {final_bracket}")
                    
                    #print(f"True for {command}")
                else:
                    for i in range((command_index + 1), (command_index + final_bracket)):
                        skip_indexes.append(i)
                    previous_if = 0
                    #print(f"False for {command}")

            elif command.strip()[:4] == "elif":
                skip_indexes = []
                open_index = find_first_char("(", command.strip()) + 1
                close_index = find_first_char(")", command.strip())

                if previous_if == -1:
                    print(f"Err - orphaned elif statement.")
                    break

                statement = evaluate_expression(command.strip()[open_index:close_index], bracketted = True)
                final_bracket = find_final_cbracket(program_commands[command_index:])

                if statement and previous_if == 0:
                    skip_indexes.append(command_index + final_bracket)
                    previous_if = 1
                else:
                    for i in range((command_index + 1), (command_index + final_bracket)):
                        skip_indexes.append(i)

            elif command.strip()[:4] == "else":
                skip_indexes = []

                if previous_if == -1:
                    print(f"Err - orphaned else statement.")
                    break

                final_bracket = find_final_cbracket(program_commands[command_index:])

                if previous_if == 0:
                    skip_indexes.append(command_index + final_bracket)
                else:
                    for i in range((command_index + 1), (command_index + final_bracket)):
                        skip_indexes.append(i)

                previous_if = -1

            elif command.strip()[:3] == "for":
                if commands[2] != "in" and commands[2] != "->":# in command.strip():
                    print(f"Err - malformed line {command.strip()}. Unable to find 'for' or '->' in 'for' loop.")
                    break
                
                variables[commands[1][1:]] = None

                open_index = find_first_char("(", command.strip()) + 1 + len(commands[1]) + len(commands[2]) + 1
                close_index = find_first_char(")", command.strip())
                iteration_item = evaluate_expression(command.strip()[open_index:close_index], bracketted = True)

                if type(iteration_item) == int:
                    iteration_item = range(iteration_item)

                if isinstance(iteration_item, Iterable):
                    final_bracket = find_final_cbracket(program_commands[command_index:])

                    for i in range((command_index + 1), (command_index + final_bracket)):
                        skip_indexes.append(i)

                    for val in iteration_item:
                        variables[commands[1][1:]] = val
                        process_lines(program_commands[command_index + 1:command_index + final_bracket])

                else:
                    print(f"Err - {iteration_item} is not iterable for 'for' loop.")
                    break

            elif command.strip()[:5] == "while":
                open_index = find_first_char("(", command.strip()) + 1
                close_index = find_first_char(")", command.strip())
                statement = evaluate_expression(command.strip()[open_index:close_index], bracketted = True)

                if isinstance(statement, bool):
                    final_bracket = find_final_cbracket(program_commands[command_index:])

                    for i in range((command_index + 1), (command_index + final_bracket)):
                        skip_indexes.append(i)

                    while statement:
                        process_lines(program_commands[command_index + 1:command_index + final_bracket])
                        statement = evaluate_expression(command.strip()[open_index:close_index], bracketted = True)

                else:
                    print(f"Err - {statement} is not compatible with 'while' loop.")
                    break
            
            elif command.strip()[:4] == "func":
                nom_open_index = find_first_char("(", commands[1].strip()) - 1
                open_index = find_first_char("(", command.strip()) + 1
                close_index = find_first_char(")", command.strip())
                final_bracket = find_final_cbracket(program_commands[command_index:])

                functions[commands[1][:nom_open_index]] = [[], []]

                func_vars = command.strip()[open_index:close_index].split(",")
                for var in func_vars:
                    functions[commands[1][:nom_open_index]][0].append(var.strip())

                for i in range((command_index + 1), (command_index + final_bracket)):
                    functions[commands[1][:nom_open_index]][1].append(program_commands[i])
                    skip_indexes.append(i)
            elif command.strip()[:6] == "return":
                if inside_function:
                    variables["$#" + inside_function] = evaluate_expression(command.strip()[7:].strip())

                else:
                    print(f"Err - orphaned return.")
                    break


            elif command.strip() not in ["{", "}", ";"]:
                open_index = find_first_char("(", command.strip()) + 1

                if commands[0].strip()[:open_index - 2] in functions:
                    pass

                else:
                    print(f"Err - {command} is not a known function.")
                    break


        command_index += 1

print(start_message.message)
process_lines(programlines)
print(f"COMPILER OUT: final vars = {variables}")
print(f"COMPILER OUT: final funcs = {functions}")
