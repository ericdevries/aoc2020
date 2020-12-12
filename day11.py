import json

with open("data/day11.txt") as f:
    lines = [list(x.strip()) for x in f]


def occupied_seats(field, i, j):
    counter = 0

    for x in range(i - 1, i + 2):
        if x < 0 or x >= len(field):
            continue

        line = field[x]

        for y in range(j - 1, j + 2):
            if y < 0 or y >= len(line):
                continue

            if x == i and y == j:
                continue

            column = line[y]

            if column == "#":
                counter += 1

    return counter


def check_range(s, i, j):
    for x in range(i, j):
        if x == "L":
            return 0

        if x == "#":
            return 1

    return 0


def check_path(field, i, j, dx, dy):
    if i < 0 or i >= len(field):
        return 0

    row = field[i]

    if j < 0 or j >= len(row):
        return 0

    part = row[j]

    if part == "L":
        return 0
    elif part == "#":
        return 1

    return check_path(field, i + dx, j + dy, dx, dy)


def check_diagonal1(field, i, j):
    s = []
    x = max(0, i - j)
    y = j - max(i - x, 0)
    # start is j - i

    line = "".join([f[j] for f in field])
    count = 0
    count += check_range(line, 0, j)
    count += check_range(line, j, len(line))

    return count


def occupied_seats_los(field, i, j):
    item = field[i][j]

    if item == ".":
        return "."

    counter = 0

    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue

            counter += check_path(field, i + x, j + y, x, y)

    if item == "L" and counter == 0:
        return "#"
    elif item == "#" and counter >= 5:
        return "L"

    return item


def pf(field):
    print(fs(field))
    print()


def fs(field):
    return "\n".join(["".join(f) for f in field])


def issame(field1, field2):
    f1 = fs(field1)
    f2 = fs(field2)

    return f1 == f2


def countseats(field):
    f = fs(field)
    f = filter(lambda s: s == "#", f)
    f = "".join(f)

    return len(f)


def gol(field):
    previous = None

    while True:
        copy = json.loads(json.dumps(field))

        for i, x in enumerate(field):
            for j, y in enumerate(x):
                column = copy[i][j]

                if column == ".":
                    continue

                occ = occupied_seats(field, i, j)

                if column == "L" and occ == 0:
                    copy[i][j] = "#"
                elif column == "#" and occ >= 4:
                    copy[i][j] = "L"

        previous = field
        field = copy

        pf(field)

        if issame(previous, field):
            print(countseats(field))
            break


def gol2(field):
    previous = None

    while True:
        copy = json.loads(json.dumps(field))

        for i, x in enumerate(field):
            for j, y in enumerate(x):
                copy[i][j] = occupied_seats_los(field, i, j)

        previous = field
        field = copy

        pf(field)

        if issame(previous, field):
            print("DONE!")
            print(countseats(field))
            break


# gol(lines)
gol2(lines)
