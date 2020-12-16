from collections import defaultdict

attrs = dict()
your_ticket = []
nearby_tickets = []

with open("data/day16.txt") as f:
    data = f.read().split("\n\n")

    for item in data[0].split("\n"):
        key, val = item.split(": ", 1)
        ranges = tuple(map(lambda s: tuple(map(int, s.split("-"))), val.split(" or ")))
        attrs[key] = ranges

    your_ticket = list(map(int, data[1].split("\n")[1].split(",")))

    for item in data[2].split("\n", 1)[1].split("\n"):
        if len(item) > 0:
            nearby_tickets.append(list(map(int, item.split(","))))

    print("ranges: ", attrs)
    print("your ticket: ", your_ticket)
    print("nearby tickets: ", nearby_tickets)


def is_valid(num):
    for a in attrs.values():
        for r in a:
            if num >= r[0] and num <= r[1]:
                return True

    return False


def task1():
    invalid = []

    for item in nearby_tickets:
        for num in item:
            if not is_valid(num):
                invalid.append(num)

    print("answer: ", sum(invalid))


def is_valid_ticket(ticket):
    return False not in list(map(is_valid, ticket))


def can_be_attr(values, ranges):
    for v in values:
        is_valid = False
        for r in ranges:
            if r[0] <= v <= r[1]:
                is_valid = True
                break

        if not is_valid:
            return False

    return True


def get_attr(values):
    result = set()

    for key, ranges in attrs.items():
        if can_be_attr(values, ranges):
            result.add(key)

    return result

def has_multiple_options(columns):
    return len(list(filter(lambda s: len(s) > 1, columns.values()))) > 0

def task2():
    valid = list(filter(is_valid_ticket, nearby_tickets))
    columns = dict()

    for i in range(len(valid[0])):
        values = set()

        for ticket in valid:
            values.add(ticket[i])
        
        columns[i] = get_attr(values)
    
    taken = set()

    while has_multiple_options(columns):
        # find all the ones where only 1 option exists
        for key, value in columns.items():
            if len(value) == 1:
                taken.add(list(value)[0])
        
        updated_columns = dict()

        for key, value in columns.items():
            if len(value) > 1:
                new_values = value.difference(taken)
            else:
                new_values = value 

            updated_columns[key] = new_values

        columns = updated_columns
    
    answer = 1

    for key, value in updated_columns.items():
        val = list(value)[0]
        
        print(val)
        if val.startswith('departure'):
            answer *= your_ticket[key]

    print('answer2: ', answer)


    print(columns)
task1()
task2()
