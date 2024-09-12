import globals


class Types:
    @staticmethod
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

    @staticmethod
    def is_comparison_operator(op : str):
        if op in ["&&", "||", "==", "!=", ">=", "<=", ">", "<"] or "~" in op:
            return True
        else:
            return False
     

    @staticmethod
    def check_next_item(item : str):
        """
        returns True if the item supplied doesn't exist.
        """
        try:
            if item not in ["+", "-", "&&", "*", "/", "%", ":", "||", "==", "!=", ">=", "<=", ">", "<"] and "~" not in item:
                next_expression = Types.convert_to_correct_type(item)
                if next_expression == None:
                    return True
        except:
            pass

        return False

    @staticmethod
    def convert_to_correct_type(item : str):
        val = None
        item = item.strip()

        if "." in item:
            try: val = float(item)
            except: pass
        elif item in globals.variables:
            val = globals.variables[item]
        elif item.isdigit():
            val = int(item)
        elif item[0] == '"' and item[-1] == '"':
            val = str(item[1:-1])


        return val


