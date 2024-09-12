from type_conversions import Types
from default_types.string_type import StringType
from default_types.float_type import FloatType
from default_types.int_type import IntType
from walking_tools.organisers import Organisers
import globals
#import evaluator #import Evaluator
from comparator import Comparator
import line_reader

class Evaluator:
    @staticmethod
    def evaluate_expression(expression : str, bracketted = False):
        #expressions = expression.split(" ")
        #expressions = collate_strings(expressions)
        if not bracketted:
            expressions = Organisers.split_organise(expression)
        else:
            expressions = Organisers.split_organise(expression, orphaned = True)

        rightItem = None
        found_full_expression = False
        last_operator = ""
        multi_store = None
        last_operators = []
        skip_indexes = []
        exp_index = 0

        #print(f"expression: {expressions}")
        if "||" in expressions or "&&" in expressions:
            #print(f"multi_store set to []")
            multi_store = []

        for exp in expressions:
            if exp_index in skip_indexes:
                exp_index += 1
                continue

            temp_right = None
            #print(f"processings {exp}")
            if found_full_expression:
                print(f"Err - expression is not comprehendable - contains too many arguments.")
                break

            if exp not in ["+", "-", "&&", "*", "/", "%", ":", "||", "==", "!=", ">=", "<=", ">", "<"] and not "~" in exp and multi_store == None:
                try:
                    found_full_expression = Types.check_next_item(expressions[exp_index + 1])
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

                    open_index = Organisers.find_first_char("(", dec_split_items[1].strip()) + 1
                    close_index = Organisers.find_first_char(")", dec_split_items[1].strip())

                    temp_func_vars = dec_split_items[1].strip()[open_index:close_index].split(",")
                    func_vars = []

                    for var in temp_func_vars:
                        func_vars.append(Evaluator.evaluate_expression(var, bracketted = True))

                    func_name = dec_split_items[1].strip()[:open_index - 1]

                    if dec_split_items[0] == "string":
                        func_return = StringType.evaluate_string_func(func_name, func_vars)
                        temp_right = func_return

                    elif dec_split_items[0] == "int":
                        func_return = IntType.evaluate_int_func(func_name, func_vars)
                        temp_right = func_return
                    elif dec_split_items[0] == "float":
                        func_return = FloatType.evaluate_float_func(func_name, func_vars)
                        temp_right = func_return



                elif exp in globals.variables:
                    val = globals.variables[exp]
                    temp_right = val

                    if not type(val) in [int, str, float]:
                        found_full_expression = True
                elif exp == "true":
                    temp_right = True

                elif exp == "false":
                    temp_right = False

                elif exp.isdigit():
                    temp_right = int(exp)

                elif is_float:
                    temp_right = float(exp)

                elif exp[0] == '"' and exp[-1] == '"':
                    temp_right = str(exp.strip('"'))

                elif exp[0] == '(':
                    if exp[1] != ')':
                        pass
                    exp_bracket_end = Organisers.find_final_bracket(expressions[exp_index + 1:], "(")
                    exp_bracket_end += exp_index + 1
                    #print(f"brackstart = {exp_index} brackend = {exp_bracket_end}")
                    #print(f"sending to evaluator {' '.join(expressions[exp_index:exp_bracket_end + 1])[1:-1]}")
                    temp_right = Evaluator.evaluate_expression(' '.join(expressions[exp_index:exp_bracket_end + 1])[1:-1], bracketted = True)
                    for i in range(exp_index + 1, exp_bracket_end + 1):
                        skip_indexes.append(i)

                else:
                    if "(" in exp:
                        open_index = Organisers.find_first_char("(", exp.strip()) + 1

                        #print(f"checking {exp.strip()[:open_index - 2]} against functions")
                        func_name = exp.strip()[:open_index - 1]
                        if func_name in globals.functions:
                            function = []
                            var_defaults = globals.functions[func_name][0]
                            for var_default in var_defaults:
                                if "=" in var_default:
                                    function.append(var_default + ";")

                            close_index = Organisers.find_first_char(")", exp.strip())
                            func_vars = exp.strip()[open_index:close_index].split(",")
                            var_num = 0
                            for func_var in func_vars:
                                function.append(var_defaults[var_num] + " = " + func_var.strip() + ";")
                                var_num += 1

                            function = function + globals.functions[func_name][1]
                            #print(f"processing lines:\n{function}")
                            line_reader.process_lines(function, func_name)
                            if last_operator == "":
                                temp_right = globals.variables["$#" + func_name]

                        else:
                            print(f"Err - expression {exp} is not comprehendable")
                            break

                
                if last_operator == "":
                    rightItem = temp_right

                elif type(rightItem) != type(temp_right):
                    print(f"Err - type {type(rightItem)} ({rightItem}) does not match type {type(temp_right)} ({temp_right})")
                    break

                elif type(rightItem) == int and type(temp_right) == int:
                    if last_operator == "+":
                        rightItem += temp_right
                    elif last_operator == "-":
                        rightItem -= temp_right
                    elif last_operator == "*":
                        rightItem = rightItem * temp_right
                    elif last_operator == "/":
                        rightItem = rightItem / temp_right
                    elif Types.is_comparison_operator(last_operator):
                        pass

                    else:
                        print(f"Err - unsupported operation ({last_operator}) for int {exp}")
                        break

                elif type(rightItem) == float and type(temp_right) == float:
                    if last_operator == "+" and type(temp_right) == float:
                        rightItem += temp_right
                    elif last_operator == "-":
                        rightItem -= temp_right
                    elif last_operator == "*":
                        rightItem = rightItem * temp_right
                    elif last_operator == "/":
                        rightItem = rightItem / temp_right
                    elif Types.is_comparison_operator(last_operator):
                        pass


                    else:
                        print(f"Err - unsupported operation ({last_operator}) for float {exp}")
                        break

                elif type(rightItem) == str and type(temp_right) == str:
                    if last_operator == "+":
                        rightItem = rightItem + temp_right
                    if last_operator == "-":
                        if rightItem[:len(temp_right)] == temp_right:
                            rightItem = rightItem[len(temp_right):]
                        elif rightItem[len(temp_right):] == temp_right:
                            rightItem = rightItem[:len(temp_right)]
                    elif Types.is_comparison_operator(last_operator):
                        pass
                
                else:
                    print(f"Err - unsupported operation ({last_operator}) between {type(rightItem)} ({rightItem}) and {type(temp_right)} ({temp_right})")

            else:
                #print(f"encountered exp {exp}")
                if not found_full_expression:
                    #print(f"multi_store = {multi_store}")
                    if multi_store == None:
                        if exp in ["==", "!=", ">=", "<=", ">", "<"] or "~" in exp:
                            try:
                                compare = Comparator.perform_comparison(expressions[exp_index - 1], exp, expressions[exp_index + 1])
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
                                    next_expression = Types.convert_to_correct_type(expressions[exp_index + 1])
                                    if next_expression:
                                        multi_store.append(True)
                                    else:
                                        multi_store.append(False)
                            except:
                                pass
                            last_operators.append(exp)
                        elif exp in ["==", "!=", ">=", "<=", ">", "<"] or "~" in exp:
                            #print(f"performing comparison {expressions[exp_index - 1] + exp + expressions[exp_index + 1]}")
                            compare = Comparator.perform_comparison(expressions[exp_index - 1], exp, expressions[exp_index + 1])
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
            current_state = multi_store[0]
            for bool_val in range(len(multi_store)):
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

            rightItem = current_state

        return rightItem


