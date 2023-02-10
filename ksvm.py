import sys

TOKENS = {
    "CPT": "cpt",
    "AND": "and",
    "OR": "or",
    "EQ": "eq",
    "GT": "gt",
    "LT": "lt",
    "LPAREN": "(",
    "RPAREN": ")",
    "IF": "if",
    "THEN": "then",
}


def OR(*args):
    return any(args)


def AND(*args):
    return all(args)


def EQ(lhs, rhs):
    return lhs == rhs


def GT(lhs, rhs):
    return lhs > rhs


def LT(lhs, rhs):
    return lhs < rhs


OPERATIONS = {"and": AND, "or": OR, "eq": EQ, "gt": GT, "lt": LT}

RUNTIME_CPTS = {}
CPT_OPTIONS = {}
CPTS = {}
RULES = []
RESULTS = {}


class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def __str__(self):
        return f"Rule({self.condition}, {self.action})"


def check_token(token):
    for key, value in TOKENS.items():
        if token == value:
            return key
    return None


def define_runtime_cpt(cpt, val):
    RUNTIME_CPTS[cpt] = val


def define_cpt_options(cpt, options):
    CPT_OPTIONS[cpt] = options


def define_cpt(cpt):
    CPTS[cpt] = cpt


def define_result(cpt, val):
    RESULTS[cpt] = val


def parse_cpt(line):
    tokens = line.split()
    cpt = tokens[1]
    options = tokens[2].split("/")
    if options[0] == "bool":
        options = ["true", "false"]
    elif options[0] == "num":
        options = ["a number"]

    define_cpt(cpt)
    define_cpt_options(cpt, options)


def parse_rule(line):
    tokens = line.split()
    if_clause = []
    then_clause = []
    token = tokens[0]
    while check_token(token) != "THEN":
        if check_token(token) == "IF":
            tokens.pop(0)
            token = tokens[0]

        if_clause.append(token)
        tokens.pop(0)
        token = tokens[0]

    then_clause.append(tokens[1])
    RULES.append(Rule(if_clause, then_clause))


def eval_rule(rule: Rule):
    if_clause = rule.condition
    then_clause = rule.action
    buffer = []
    rule_stack = []
    i = 0
    while i < len(if_clause):
        cur_token = if_clause[i]

        # if rule operation inside parentheses
        if "(" in cur_token:
            cur_token = if_clause[i].replace("(", "")
            while ")" not in cur_token:
                buffer.append(cur_token)
                i += 1
                cur_token = if_clause[i]
            cur_token = if_clause[i].replace(")", "")
            buffer.append(cur_token)
            rule_stack.append(eval_operation(buffer))
            buffer.clear()
            if i + 1 < len(if_clause):
                i += 1
                cur_token = if_clause[i]
            else:
                break
            if cur_token in list(OPERATIONS.keys()):
                rule_stack.append(cur_token)
                i += 1
                continue
        # if rule operation
        buffer.append(cur_token)
        i += 1
        continue
    if len(buffer) > 0:
        rule_stack.append(eval_operation(buffer))

    if len(rule_stack) > 1:
        final_result = eval_operation(rule_stack)
        rule_stack.clear()
        rule_stack.append(final_result)

    # put result in runtime CPT
    define_runtime_cpt(then_clause[0], rule_stack[0])
    define_result(then_clause[0], rule_stack[0])


def eval_operation(operation):
    if len(operation) == 3:
        lhs, op, rhs = operation
    elif len(operation) > 3:
        return eval_multi_operation(operation)
    try:
        lhs = RUNTIME_CPTS[lhs] if lhs != True and lhs != False else lhs
    except KeyError:
        print(f"ERROR: {lhs} is not a defined concept")
        sys.exit()
    rhs = True if rhs == "true" else rhs
    rhs = False if rhs == "false" else rhs

    rhs = is_number(rhs)[1] if is_number(rhs)[0] else rhs
    return OPERATIONS[op](lhs, rhs)


def eval_multi_operation(operation):
    operants = []
    if (TOKENS["AND"] in operation) and not (TOKENS["OR"] in operation):
        for i in range(len(operation)):
            if operation[i] != TOKENS["AND"]:
                operants.append(operation[i])
        return AND(*operation)
    elif (TOKENS["OR"] in operation) and not (TOKENS["AND"] in operation):
        for i in range(len(operation)):
            if operation[i] != TOKENS["OR"]:
                operants.append(operation[i])
        return OR(*operants)


def is_number(s):
    try:
        n = float(s)
        return True, n
    except ValueError:
        return False, None


def is_bool(s):
    if s == "true":
        return True, True
    elif s == "false":
        return True, False
    else:
        return False, None


def user_input():
    for key, value in CPTS.items():
        ops = str(CPT_OPTIONS[key]).replace("'", "")
        u_in = input(f"{key}: {ops} = ")
        if CPT_OPTIONS[key] == ["true", "false"]:
            while not is_bool(u_in)[0]:
                print("Please enter true or false")
                u_in = input(f"{key}: {ops} = ")
            define_runtime_cpt(key, is_bool(u_in)[1])
        elif CPT_OPTIONS[key] == ["a number"]:
            while not is_number(u_in)[0]:
                print("Please enter a valid number")
                u_in = input(f"{key}: {ops} = ")
            define_runtime_cpt(key, is_number(u_in)[1])
        else:
            while u_in not in CPT_OPTIONS[key]:
                print("Please enter a valid option")
                u_in = input(f"{key}: {ops} = ")
            define_runtime_cpt(key, u_in)


def syntax_error(line):
    print(f"ERROR: Syntax error in line {line}")
    sys.exit()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("ERROR: Please provide a .ks file")
        exit()
    ks_arg = sys.argv[1]
    if ".ks" not in ks_arg:
        print("ERROR: Please provide a valid .ks file")
        exit()
    try:
        ks_file = open(ks_arg, "r").readlines()
    except FileNotFoundError:
        print("ERROR: File not found")
        exit()
    for i, line in enumerate(ks_file):
        if line == "\n":
            continue
        first_token = line.split()[0]
        if check_token(first_token) == "CPT":
            parse_cpt(line)
        elif check_token(first_token) == "IF":
            try:
                parse_rule(line)
            except IndexError:
                syntax_error(i + 1)
        else:
            syntax_error(i + 1)

    user_input()
    for rule in RULES:
        eval_rule(rule)

    print(RESULTS)
