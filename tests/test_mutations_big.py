import random
import codecs
import json
import numpy as np
from individual import Individual


def i2s(i, d=2):
    res = str(i)
    return "0" * (d - len(res)) + res


def read_setup(fname):
    """
        Reads the setup from the input file 'fname'.
        pizza -- 2D list of pizza contents
        n_row, n_col -- number of rows and columns in pizza
        L -- minimum amount of each ingridient in a slice
        H -- maximum size of a slice
    """
    with codecs.open(fname, 'r') as fin:
        n_row, n_col, L, H = list(map(int, fin.readline().split()))

        pizza = []
        for _ in range(n_row):
            line = fin.readline().strip()
            pizza.append(line)

    return pizza, n_row, n_col, L, H


def generate_possible_slices(L, H):
    """
        Generates a list of all possible slices based on L and H.
        Each slice is encoded as (wi, he) - it's width and height, respectively.
    """
    n_min = 2 * L
    n_max = H

    slices = []
    for he in range(1, n_max+1):
        for wi in range(max(1, n_min // he), n_max + 1):
            if he * wi > n_max:
                break
            slices.append((wi, he))

    return slices


start = 501
end = 1001

res_path = "results_big/"
pizza, n_row, n_col, L, H = read_setup("input/d_big.in") # a_example  b_small  c_medium  d_big
slices = generate_possible_slices(L, H)


# A = Individual({}, slices, n_col, n_row, L, H)
# A.load_layout(res_path+"000000.json", pizza)
# print(A)

# B = Individual({}, slices, n_col, n_row, L, H)
# B.load_layout(res_path+"000250.json", pizza)
# print(B)

def load_lay(fname):
    with codecs.open(fname, 'r') as fin:
            _lay = json.load(fin)
    res = {}
    for pos in _lay:
        res[int(pos)] = _lay[pos]
    return res


scores = []
if start == 0:
    A = Individual({}, slices, n_col, n_row, L, H)
    A.fill_layout(pizza)
    scores.append((0, A.efficiency()))
else:
    A_lay = load_lay(res_path+"%s.json"%i2s(start-1,6))
    A = Individual(A_lay, slices, n_col, n_row, L, H)
    assert(A.check_correctness(pizza))

for i in range(start, end):
    print(i, end='; ')
    B = A.copy()
    B.mutate(pizza)
    if B > A:
        print("%7.4f -> %7.4f"%(A.efficiency(), B.efficiency()), end='')
        scores.append((i, B.efficiency()))
        A = B.copy()
    print()

    if i % 250 == 0:
        A.dump_layout(res_path+"%s.json"%i2s(i,6))

with codecs.open(res_path+"convergence.txt", "a") as fout:
    for i, eff in scores:
        fout.write("%s; %7.4f\n"%(i2s(i, 4), eff))


########################################################
########################################################
# A = Individual({}, slices, n_col, n_row, L, H)
# A.fill_layout(pizza)
# best = A.score()
# for i in range(100):
#     B = Individual({}, slices, n_col, n_row, L, H)
#     B.fill_layout(pizza)
#     if B.score() > best:
#         A = B.copy()
#         best = B.score()
#         print("%d, current best:"%i, A)

# A.dump_layout(res_path+"best_00.json")



