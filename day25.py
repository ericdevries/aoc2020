
def calc_ls(num, expected):
    val = 1
    loopsize = 0

    while True:
        val = val * num
        rem = val % 20201227
        val = rem
        
        loopsize += 1

        if val == expected:
            break

    return loopsize

def transform(num, ls):
    val = 1
    for i in range(ls):
        val = val*num
        val = val % 20201227
    
    return val

def task1():
    inp = [5764801, 17807724]
    inp = [14222596, 4057428]

    
    ls1 = calc_ls(7, inp[0])
    ls2 = calc_ls(7, inp[1])
    
    ek1 = transform(inp[0], ls2)
    ek2 = transform(inp[1], ls1)

    assert ek1 == ek2
    print(ls1, ls2)
    print('answer1: %s' % ek1)
    breakpoint()


task1()




