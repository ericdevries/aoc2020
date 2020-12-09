PREAMBLE = 25

with open("./data/day9.txt") as f:
    data = f.read()
    data = data.split("\n")
    data = filter(lambda s: len(s) > 0, data)
    data = map(int, data)


def check_index(data, i):
    items = data[max(0, i - PREAMBLE) : i]
    item = data[i]

    return is_multiple(items, item)


def is_multiple(data, value):
    for i, x in enumerate(data):
        for j, y in enumerate(data):
            if i == j:
                continue

            if x + y == value:
                return True

    return False


data = list(data)


def part1():
    for i in range(PREAMBLE, len(data)):
        value = data[i]
        valid = check_index(data, i)

        if not valid:
            print("not valid", value)
            return value


def is_valid_sum(data, value):
    for i, x in enumerate(data):
        subset = data[:i]
        result = sum(subset)

        if result > value:
            break

        if result == value:
            return subset

    return False


def part2(value):
    for i in range(len(data)):
        subset = data[i:]
        valid = is_valid_sum(subset, value)

        if valid:
            print(valid)
            print('result is', min(valid) + max(valid))


value = part1()
part2(value)
