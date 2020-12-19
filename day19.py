import pprint
import re

with open("data/day19.txt") as f:
    rule_data, test_data = f.read().split("\n\n", 1)
    # rule_data, test_data = [x.strip() for x in f]
rule_list = [f.strip() for f in rule_data.split("\n")]
test_list = [f.strip() for f in test_data.split("\n") if len(f.strip()) > 0]

rules = dict()
raw_rules = dict()

for item in rule_list:
    num, d = item.split(":", 1)
    res = []

    for subrules in d.strip().split("|"):
        res.append(subrules.strip().split(" "))

    rules[num] = res
    raw_rules[num] = d.strip().split(" ")
# print(test_list)


def substitute(rule):
    global rules
    if type(rule) == list:
        return list(map(substitute, rule))

    if rule.isdigit():
        return substitute(rules.get(rule))

    return rule[1]


def flatten(rule):
    if type(rule) != list:
        return rule

    if type(rule) == list and len(rule) == 1:
        return flatten(rule[0])

    return list(map(flatten, rule))


def permutate(rule):
    if len(rule) == 0:
        yield ""

    elif type(rule) == str:
        yield rule

    else:
        print("oh my")
        for x in permutate(rule[0]):
            for y in permutate(rule[1:]):
                yield x + y


def unparse(rule):
    if type(rule) == str:
        return rule

    if len(rule) == 0:
        return ""


def matches_rule(rule_num, line):
    rule = rules.get(rule_num)
    subs = substitute(rule)
    flattened = flatten(subs)

    print(flattened)
    breakpoint()
    print(permutate(flattened))
    for s in permutate(flattened):
        print("hello", s)
    pprint.pprint(subs)
    breakpoint()
    print(substitute(rule))
    print(rule_num, line)


def regextest(rule):
    res = []
    append_final = False
    for item in rule:
        if item.isdigit():
            res.append(regextest(raw_rules[item]))
        elif item == "|":
            res.insert(0, "(")
            res.append("|")
            append_final = True
        else:
            res.append(item.replace('"', ""))

    if append_final:
        res.append(")")

    return "".join(res)


def task1():
    rule = "^" + regextest(raw_rules["0"]) + "$"
    count = 0

    print(rule)
    for item in test_list:
        test_str = re.match(rule, item)

        if test_str is not None:
            count += 1

    print("answer: %s" % count)


def regextest2(rule):
    res = []
    append_final = False

    for item in rule:
        if item == "8":
            res.append("(")
            res.append(regextest2(raw_rules[item]))
            res.append(")+")
        elif item == "11":
            rule2 = raw_rules["11"]
            rule_a = regextest2(raw_rules[rule2[0]])
            rule_b = regextest2(raw_rules[rule2[1]])
            max_len = int(max([len(l) for l in test_list]) / 2)
            new_rules = "|".join(
                ["%s{%s}%s{%s}" % (rule_a, i, rule_b, i) for i in range(1, max_len - 1)]
            )
            res.append("(")
            res.append(new_rules)
            res.append(")")

        elif item.isdigit():
            res.append(regextest2(raw_rules[item]))
        elif item == "|":
            res.insert(0, "(")
            res.append("|")
            append_final = True
        else:
            res.append(item.replace('"', ""))

    if append_final:
        res.append(")")

    return "".join(res)


def task2():
    # raw_rules["11"] = "42 31 | 42 11 31".split(" ")
    # raw_rules["8"] = "42 | 42 8".split(" ")

    rule = "^" + regextest2(raw_rules["0"]) + "$"
    count = 0

    for item in test_list:
        test_str = re.match(rule, item)

        if test_str is not None:
            count += 1

    print("answer2: %s" % count)


task1()
task2()
