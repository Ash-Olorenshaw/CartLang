from type_conversions import Types

class Comparator:
    @staticmethod
    def perform_comparison(item1 : str, comparator : str, item2 : str):
        return_val = False

        if type(item1) == str:
            first_item = Types.convert_to_correct_type(item1)
        else:
            first_item = item1
        if type(item2) == str:
            second_item = Types.convert_to_correct_type(item2)
        else:
            second_item = item2

        if type(first_item) == type(second_item):


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
        else:

            print(f"Err - type '{type(first_item)}' does not match '{type(second_item)}'")
            return -1



