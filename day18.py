import json

with open("data/day18.txt") as f:
    lines = [x.strip().replace(" ", "") for x in f if len(x) > 0]


# change 5+(8*3+9+3*4*3)
# into   5+(((((8*3)+9)+3)*4)*3)

# change 5*9*(7*3*3+9*3+(8+6*4))
# into   (5*9)*(((((7*3)*3)+9)*3)+((8+6)*4))


def tokenize(s):
    num = []

    for c in s:
        if not c.isdigit():
            if len(num) > 0:
                yield "".join(num)
            num = []
            yield c
        else:
            num.append(c)

    if len(num) > 0:
        yield "".join(num)


def parseline(s):
    num = None
    op = None

    tokens = [t for t in tokenize(s)]
    offset = 0

    for i in range(len(tokens)):
        if i + offset >= len(tokens):
            break
        c = tokens[i + offset]
        if c == "(":
            next_num, skip = parseline(tokens[i + offset + 1 :])
            offset += skip
            if num is None:
                num = next_num
            else:
                num = eval("%s %s %s" % (num, op, next_num))
        elif c == ")":
            return num, i + offset + 1
        elif c.isnumeric():
            if num is None:
                num = int(c)
            else:
                num = eval("%s %s %s" % (num, op, c))
        else:
            op = c

    return num, 0


def processblock(s):
    if type(s) != list:
        return s

    if len(s) == 0:
        return []

    if len(s) < 3:
        return s

    new_items = list(map(processblock, s))
    result = []
    pos = 0

    while pos < len(new_items):
        item = new_items[pos]

        if item == "+":
            p1 = result[-1]
            result = result[:-1]
            result.append([p1, item, new_items[pos + 1]])
            pos += 2

        else:
            result.append(item)
            pos += 1

    return result


def calculate_item(item):
    num = None
    op = None

    for i in item:
        if type(i) == list:
            i = calculate_item(i)

        if type(i) == int:
            if op == "+":
                num += i
                op = None
            elif op == "*":
                num *= i
                op = None
            else:
                num = i
        else:
            op = i
    
    return num


def parseline3(s):
    s = s.replace("(", "[")
    s = s.replace(")", "]")
    s = s.replace("*", ',"*",')
    s = s.replace("+", ',"+",')

    items = json.loads("[%s]" % s)
    new_items = processblock(items)
    
    return calculate_item(new_items)

def task1():
    results = []
    for line in lines:
        parsed, _ = parseline(line)
        print("%s: %s" % (line, parsed))
        results.append(parsed)

    print("answer: %s" % sum(results))


def task2():
    results = []
    ## lines= ['5+(8*3+9+3*4*3)']
    #lines = ["((2+4*9)*(6+9*8+6)+6)+2+4*2"]
    for line in lines:
        parsed = parseline3(line)
        results.append(parsed)
        print(
            "%s: %s"
            % (
                line,
                parsed,
            )
        )
        print()

    print("answer: %s" % sum(results))


# task1()
task2()
