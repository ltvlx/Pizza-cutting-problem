import random
import codecs
import json
import numpy as np
from individual import Individual
import os
random.seed(0)


resume = False
i_start = 0
G_max = 5000
P = 200
c_par = 0.20
c_rec = 0.10
c_mut = 0.70
c_ran = 0.00
s = c_par + c_rec + c_mut + c_ran
c_par /= s
c_rec /= s
c_mut /= s
c_ran /= s

inp_fpath = "input/d_big.in" # a_example  b_small  c_medium  d_big
res_path = "results_big/"
for path in [res_path, res_path+'generations_backup/', res_path+'history_best/']:
    if not os.path.exists(path):
        os.makedirs(path)


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


def make_next_generation(population, pizza):
    mating_pool = population[:int(c_par * P)]

    next_generation = []
    for _ in range(int(c_rec * P) // 2):
        A, B = random.sample(mating_pool, 2)
        C, D = A.recombine(B, pizza)
        next_generation += [C, D]

    next_generation += mating_pool

    for _ in range(int(c_mut * P)):
        A = random.choice(next_generation)
        levels = random.choice([1,2,3])
        B = A.copy()
        B.mutate(pizza, levels)
        next_generation.append(B)

    for _ in range(int(c_ran * P)):
        A = Individual({}, slices, n_col, n_row, L, H)
        A.fill_layout(pizza)
        next_generation.append(A)

    next_generation.sort(key = lambda x: x.efficiency(), reverse=True)
    return next_generation


def save_population(population, G_n):
    res = []
    for ind in population:
        res.append(list(ind.layout.items()))

    with codecs.open(res_path+"generations_backup/G_%s.json"%i2s(G_n, 4), 'w') as fout:
        json.dump(res, fout)


def load_population(fname, slices, n_col, n_row, L, H, pizza):
    population = []
    with codecs.open(fname, 'r') as fin:
        layouts = json.load(fin)

    for s_list in layouts:
        _lay = {}
        for pos, k in s_list:
            _lay[tuple(pos)] = k
        A = Individual(_lay, slices, n_col, n_row, L, H)
        population.append(A)

    return population


pizza, n_row, n_col, L, H = read_setup(inp_fpath)
slices = generate_possible_slices(L, H)

if resume == False:
    population = []
    for i in range(P):
        A = Individual({}, slices, n_col, n_row, L, H)
        A.fill_layout(pizza)
        population.append(A)
    population.sort(key = lambda x: x.efficiency(), reverse=True)
else:
    print("Continuing previous optimization.")
    population = load_population(res_path + "generations_backup/G_%s.json"%i2s(i_start, 4), slices, n_col, n_row, L, H, pizza)
    print(len(population), P)
    if len(population) < P:
        print("Loaded population is smaller than the given max population.\nExtending it with random individuals.")
        while len(population) < P:
            A = Individual({}, slices, n_col, n_row, L, H)
            A.fill_layout(pizza)
            population.append(A)
        population.sort(key = lambda x: x.efficiency(), reverse=True)
    elif len(population) > P:
        print("Loaded population is bigger than the given max population.\nRemoving the worst individuals.")
        population.sort(key = lambda x: x.efficiency(), reverse=True)
        population = population[:P]


scores = []
for i in range(i_start+1, G_max):
    population = make_next_generation(population, pizza)
    eff_max = population[0].efficiency()
    scores.append((i, eff_max))

    print("%s; %7.4f%%"%(i2s(i, 4), eff_max))

    population[0].dump_layout(res_path+"history_best/G_%s_i001.txt"%i2s(i, 4))

save_population(population, i)
with codecs.open(res_path+"opt_convergence.txt", "a") as fout:
    for i, eff in scores:
        fout.write("%s; %7.4f\n"%(i2s(i, 4), eff_max))

