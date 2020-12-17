import copy

with open("data/day17.txt") as f:
    data = f.read().split("\n")
    data = [list(d) for d in data if len(d) > 0]

state = {0: data}


def expand_field(state):
    new_state = [["."] + s + ["."] for s in state]
    new_state.append(list("." * len(new_state[0])))
    new_state.insert(0, list("." * len(new_state[0])))

    return new_state


def expand_fields(state):
    new_state = {}

    for k, v in state.items():
        new_state[k] = expand_field(v)

    keys = state.keys()
    new_size = len(new_state[0])
    new_field = ["." * new_size for x in range(new_size)]
    new_state[min(keys) - 1] = new_field
    new_state[max(keys) + 1] = new_field

    return new_state


def active_count(field, pre, nex, x, y):
    fields = [pre, field, nex]
    counter = 0

    for z, f in enumerate(fields):
        if not f:
            continue
        for x1 in range(x - 1, x + 2):
            for y1 in range(y - 1, y + 2):
                if z == 1 and x1 == x and y1 == y:
                    continue

                if x1 < 0:
                    continue
                elif x1 >= len(f):
                    continue

                if y1 < 0:
                    continue
                elif y1 >= len(f[x1]):
                    continue

                c = f[x1][y1]

                if c == "#":
                    counter += 1

    return counter


def create_field(num):
    items = []

    for x in range(num):
        items.append(list("." * num))

    return items


def calculate_field(field, state, index):
    field = state.get(index)
    pre = state.get(index - 1)
    nex = state.get(index + 1)

    if not field:  # or not pre or not nex:
        return None

    new_field = create_field(len(field))
    # pf(pre)
    # pf(field)
    # pf(nex)

    count_rows = []

    for i, row in enumerate(field):
        count_row = []

        for j, col in enumerate(row):
            count = active_count(field, pre, nex, i, j)

            if col == "#" and count in (
                2,
                3,
            ):
                new_col = "#"
            elif col == "." and count == 3:
                new_col = "#"
            else:
                new_col = "."

            new_field[i][j] = new_col
            count_row.append(count)

        count_rows.append(count_row)

    # pf(field)
    # pf(new_field)
    # pf(count_rows)

    return new_field


def pf(field):
    for row in field:
        print("".join([str(s) for s in row]))

    print()


def task1():
    global state
    start = 0
    state = expand_fields(state)

    for i in range(6):
        new_state = {}

        print("CYCLE %s" % i)
        for k, v in state.items():
            new_field = calculate_field(v, state, k)

            if new_field:
                new_state[k] = new_field

        pf(state[-1])
        pf(state[0])
        pf(state[1])

        state = expand_fields(new_state)

    count = 0

    for v in state.values():
        for row in v:
            for col in row:
                if col == "#":
                    count += 1

    print("answer1: ", count)


def generate_empty_field(dim):
    result = [[list("." * dim) for x in range(dim)] for y in range(dim)]
    return result


def expand_fields2(state):
    dim = len(state[0][0][0]) + 2
    new_state = []
    new_state.append(generate_empty_field(dim))

    for i, x in enumerate(state):
        res1 = []
        res1.append(generate_empty_field(dim))

        for j, y in enumerate(x):
            f = expand_field(y)
            res1.append(f)

        res1.append(generate_empty_field(dim))
        new_state.append(res1)

    new_state.append(generate_empty_field(dim))
    return new_state


def check_structure(data, dim):
    if len(data) != dim:
        print("expected %s, got %s" % (dim, len(data)))
    for x in data:
        if len(x) != dim:
            print(" - expected %s, got %s" % (dim, len(x)))
        for y in x:
            if len(y) != dim:
                print("   - expected %s, got %s" % (dim, len(y)))
            for z in y:
                if len(z) != dim:
                    print("     - expected %s, got %s" % (dim, len(z)))
                for o in z:
                    if type(o) != str:
                        print("       - expected a string, got a list" % (o))


def get_state_count4(state, a, b, c, d):
    count = 0

    for i in range(a - 1, a + 2):
        for j in range(b - 1, b + 2):
            for k in range(c - 1, c + 2):
                for l in range(d - 1, d + 2):
                    if i == a and j == b and k == c and l == d:
                        continue

                    if i < 0 or i >= len(state):
                        continue
                    if j < 0 or j >= len(state[i]):
                        continue
                    if k < 0 or k >= len(state[i][j]):
                        continue
                    if l < 0 or l >= len(state[i][j][k]):
                        continue
                    s = state[i][j][k][l]
                    
                    #if type(s) != str:
                    #    breakpoint()
                    #print(i, j, k, l, s)
                    if s == '#':
                        count += 1

    return count


def count_cubes(arr):
    if type(arr) == list:
        return sum(map(count_cubes, arr))
    if arr == "#":
        return 1
    return 0


def task2():
    size = len(data[0])
    empty = generate_empty_field(size)[0]
    empty_row = [empty, empty, empty]
    state = [empty_row, [empty, data, empty], empty_row]
    check_structure(state, size)
    state = expand_fields2(state)

    for cycle in range(6):
        new_state = copy.deepcopy(state)
        dim = len(state)
        
        for a in range(len(state)):
            for b in range(len(new_state[a])):
                for c in range(len(new_state[a][b])):
                    for d in range(len(new_state[a][b][c])):
                        val = new_state[a][b][c][d]
                        count = get_state_count4(state, a, b, c, d)

                        if val == "#" and count in (2, 3):
                            new_state[a][b][c][d] = "#"
                        elif val == "." and count == 3:
                            new_state[a][b][c][d] = "#"
                        else:
                            new_state[a][b][c][d] = "."

        state = expand_fields2(new_state)

    print('answer: %s' % count_cubes(state))


task1()
task2()
