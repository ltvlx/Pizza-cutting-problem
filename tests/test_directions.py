import timeit

def generate_lrud(n_row, n_col):
    for y in range(n_row):
        for x in range(n_col):
            yield (x, y)

def generate_udlr(n_row, n_col):
    for x in range(n_col):
        for y in range(n_row):
            yield (x, y)

def generate_rldu(n_row, n_col):
    for y in range(n_row-1, -1, -1):
        for x in range(n_col-1, -1, -1):
            yield (x, y)

def generate_durl(n_row, n_col):
    for x in range(n_col-1, -1, -1):
        for y in range(n_row-1, -1, -1):
            yield (x, y)



def generate_walk_by(n_row, n_col, key='lrud'):
    if key == 'lrud':
        return generate_lrud(n_row, n_col)
    elif key == 'udlr':
        return generate_udlr(n_row, n_col)
    elif key == 'rldu':
        return generate_rldu(n_row, n_col)
    elif key == 'durl':
        return generate_durl(n_row, n_col)

def generate_walk(n_row, n_col, key='lrud'):
    if key == 'lrud':
        for y in range(n_row):
            for x in range(n_col):
                yield (x, y)
    elif key == 'udlr':
        for x in range(n_col):
            for y in range(n_row):
                yield (x, y)
    elif key == 'rldu':
        for y in range(n_row-1, -1, -1):
            for x in range(n_col-1, -1, -1):
                yield (x, y)
    elif key == 'durl':
        for x in range(n_col-1, -1, -1):
            for y in range(n_row-1, -1, -1):
                yield (x, y)


def f(n):
    for x, y in generate_walk_by(n, n, 'durl'):
        z = x+y

def g(n):
    for x, y in generate_walk(n, n, 'durl'):
        z = x+y


print("f:", min(timeit.repeat("for x in range(300): f(x)", "from __main__ import f", number=10)))
print("g:", min(timeit.repeat("for x in range(300): g(x)", "from __main__ import g", number=10)))

