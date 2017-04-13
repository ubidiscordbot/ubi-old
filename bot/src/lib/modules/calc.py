
def check_format(string):
    allowed = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '^', '%', '/', '+', '-', '.', ' ']
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['+', '-', '*', '/', '^', '%', '.', ' ']
    math_symbols = ['+', '-', '*', '/', '^', '%']
    i = 0
    while i > len(string):
        if i != len(string):
            if string[i] in symbols and string[i + 1] in symbols:
                print('error1')
                return False
        if string[i] not in allowed:
            print('error2')
            return False
        if string[i] in math_symbols:
            if string[i - 1] != " " or string[i + 1] != " ":
                if string[i] != "-":
                    print('error3')
                    return False
                elif string[i - 1] != " " or string[i + 1] not in nums:
                    print('error3')
                    return False
        i += 1
    return True


def make_array(p):
    all_operators = ['+', '-', '/', '*', '%', '^']
    i = 0
    current_num = ''
    new_list = []
    while i < len(p):
        if p[i] != ' ':
            current_num += str(p[i])
        else:
            new_list.append(float(current_num))
            current_num = ''
            i += 1
            new_list.append(p[i])
            i += 1
        i += 1
    new_list.append(float(current_num))
    return new_list


def solve_super_superior(li):
    i = 0
    cached_list = li
    so = ['^']
    while '^' in cached_list:
        if cached_list[i + 1] in so:
            if cached_list[i + 1] == '^':
                num1 = cached_list[i]
                num2 = cached_list[i + 2]
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.insert(i, num1 ** num2)
        if len(cached_list) > i + 2:
            if cached_list[i + 1] not in so:
                i += 1
    return cached_list


def solve_superior(li):
    i = 0
    cached_list = li
    so = ['*', '/', '%']
    while '*' in cached_list or '/' in cached_list or '%' in cached_list:
        if cached_list[i + 1] in so:
            if cached_list[i + 1] == '*':
                num1 = cached_list[i]
                num2 = cached_list[i + 2]
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.insert(i, num1 * num2)
            elif cached_list[i + 1] == '/':
                num1 = cached_list[i]
                num2 = cached_list[i + 2]
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.pop(i)
                if num1 != 0 and num2 != 0:
                    cached_list.insert(i, num1 / num2)
                else:
                    cached_list.insert(i, 1)
            else:
                num1 = cached_list[i]
                num2 = cached_list[i + 2]
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.insert(i, num1 % num2)
        if len(cached_list) > i + 2:
            if cached_list[i + 1] not in so:
                i += 1
    return cached_list


def solve_inferior(li):
    i = 0
    cached_list = li
    so = ['+', '-']
    while '+' in cached_list or '-' in cached_list:
        if cached_list[i + 1] in so:
            if cached_list[i + 1] == '+':
                num1 = cached_list[i]
                num2 = cached_list[i + 2]
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.insert(i, num1 + num2)
            else:
                num1 = cached_list[i]
                num2 = cached_list[i + 2]
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.pop(i)
                cached_list.insert(i, num1 - num2)
        if len(cached_list) > i + 2:
            if cached_list[i + 1] not in so:
                i += 1
    return cached_list


def solve_problem(p):
    starting_list = make_array(p)
    list1 = solve_super_superior(starting_list)
    list2 = solve_superior(list1)
    final_ = solve_inferior(list2)
    return final_[0]


def main(message):
    l = list(message.content)
    i = 0
    while i < 6:
        l.pop(0)
        i += 1
    string = ''.join(l)
    if check_format(string):
        try:
            return [["text", "```Answer: " + str(solve_problem(string)) + "```"]]
        except Exception:
            return [["text", "```Failed to calculate, problem seems to be in the wrong format```"]]
    else:
        return [["text", "Failed to calculate, problem seems to be in the wrong format"]]
