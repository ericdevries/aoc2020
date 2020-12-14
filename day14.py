with open("data/day14.txt") as f:
    lines = [x.strip() for x in f]

instructions = []

for line in lines:
    if line.startswith("mask = "):
        instructions.append(("mask", line[7:]))

    else:
        mem, num = line.split(" = ")
        pos = mem.split("[")[1][:-1]

        instructions.append(("mem", int(pos), int(num)))


def apply(num, mask):
    num = "0" * (len(mask) - len(num)) + num
    ret = []

    for n, m in zip(num, mask):
        if m == "X":
            ret.append(n)
        else:
            ret.append(m)

    return int("".join(ret), 2)


def get_masks(mask, level):
    if "X" not in mask:
        return set([mask])

    result = set()

    for i, c in enumerate(mask):
        if c == "X":
            start = mask[:i]
            end = mask[i + 1 :]
            result = result.union(get_masks(start + "0" + end, level+1))
            result = result.union(get_masks(start + "1" + end, level+1))
            break
    
    return result


def apply2(pos, mask):
    pos = "0" * (len(mask) - len(pos)) + pos
    ret = []

    for n, m in zip(pos, mask):
        if m == "0":
            ret.append(n)
        elif m == "1":
            ret.append(m)
        else:
            ret.append("X")
    
    ss = "".join(ret)
    output = set()
    
    masks = get_masks(ss, 1)
    
    for m in masks:
        output.add(int(m, 2))
    
    return output


def task1():
    mask = None
    values = dict()

    for item in instructions:
        if item[0] == "mask":
            mask = item[1]

        elif item[0] == "mem":
            num = bin(item[2])[2:]
            new_num = apply(num, mask)

            values[item[1]] = new_num
            print(num)
            print(new_num)

    print(values)
    print("answer1: %s" % (sum(values.values())))


def task2():
    mask = None
    values = dict()

    for item in instructions:
        if item[0] == "mask":
            mask = item[1]

        elif item[0] == "mem":
            num = item[2]
            pos = bin(item[1])[2:]
            new_pos = apply2(pos, mask)

            for p in new_pos:
                values[p] = num
           
    print('answer2: %s' % (sum(values.values())))
    breakpoint()

task1()
task2()
