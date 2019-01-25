import random
import codecs


def read_setup(fname):
    with codecs.open(fname, 'r') as fin:
        n_row, n_col, L, H = list(map(int, fin.readline().split()))

        pizza = []
        for _ in range(n_row):
            line = fin.readline().strip()
            pizza.append(line)

    return pizza, n_row, n_col, L, H


def generate_possible_slices(_L, _H):
    n_min = 2 * _L
    n_max = _H

    slices = []
    for h in range(1, n_max+1):
        for l in range(max(1, n_min // h), n_max + 1):
            if h*l > n_max:
                break
            slices.append((l,h))

    return slices


def exceeds_boundary(x, y, l, h, n_row, n_col):
    return (x+l > n_col) or (y+h > n_row)


def collides_w_used(c_used, x, y, l, h):
    for i in range(y, y+h):
        for j in range(x, x+l):
            c = j + i * n_col
            if c_used[c]:
                return True
    return False


def enough_contents(pizza, _L, x, y, l, h):
    T = 0
    M = 0
    
    for i in range(y, y+h):
        for j in range(x, x+l):
            v = pizza[i][j]
            # assert(v in ['T', 'M'])
            if v == 'T':
                T += 1
            else:
                M += 1

    return (T >= _L) and (M >= _L)


def generate_layout(c_empty, c_used, n_col, n_row):
    layout = []
    for pos in range(n_row * n_col):
        if not c_empty[pos]:
            continue
        # # Random chance to leave the cell unused without even trying to fit anything here 
        # # First, prove that this is necessary
        # if random.random() < 0.1:
        #     print("Randomly skipping %d"%pos)
        #     c_used[pos] = 1
        #     c_empty[pos] = 0
        #     continue
        
        y = pos // n_col
        x = pos - y * n_col

        # Trying to place each type of slice in a random order
        i_slice = [i for i in range(len(slices))]
        random.shuffle(i_slice)
        for k in i_slice:
            l, h = slices[k]
            if exceeds_boundary(x, y, l, h, n_row, n_col) or collides_w_used(c_used, x, y, l, h) or not enough_contents(pizza, _L, x, y, l, h):
                # Impossible to place slice k here
                continue
            else:
                # Placing the slice
                layout.append((pos, k))
                for i in range(y, y+h):
                    for j in range(x, x+l):
                        c = j + i * n_col
                        c_used[c] = 1
                        c_empty[c] = 0
                break
    return c_empty, c_used, layout



# pizza, n_row, n_col, _L, _H = read_setup("a_example.in")
pizza, n_row, n_col, _L, _H = read_setup("b_small.in")
# pizza, n_row, n_col, _L, _H = read_setup("c_medium.in")
# pizza, n_row, n_col, _L, _H = read_setup("d_big.in")

slices = generate_possible_slices(_L, _H)

# print("Slices: ", slices)
# for row in pizza:
#     print(row)

print("Max score is %d"%(n_col * n_row))
scores = []
# random.seed(0)
for i in range(1):
    if i % 500 == 0:
        print("  i = %d"%i)
    """
    c_empty --  cells that are empty and a slice can use them
    c_used  --  cells that are occupied by either a slice, or by randomly assigned unused cell
                it might be necessary in future to have a different list for unused cells
    layout  --  gene of an individual encoded as tuples (pos, k)
                pos is the position on the pizza, 0 <= pos <= n_col * n_row - 1
                k is the index of slice that has its upper left cell at this pos
    """
    c_empty = [1 for _ in range(n_row * n_col)]
    c_used = [0 for _ in range(n_row * n_col)]

    c_empty, c_used, layout = generate_layout(c_empty, c_used, n_col, n_row)


        
    efficiency = 100 * (1 - sum(c_empty) / n_row / n_col)
    scores.append(efficiency)
    print("The efficiency of the created layout = %5.2f%%; score is %d"%(efficiency, sum(c_used)))
    print(layout)


    # if efficiency > 99.0:
        # print("SUCCESS on iteration %d!"%i)
        # print(layout)
        # break

# for i in range(len(slices)):
#     print(i, slices[i])


"""
def draw_hist():
    # Draw the goal function histogram
    import numpy as np
    import matplotlib.pyplot as plt


    def halven_bins(b):
        res = []
        for i in range(len(b)-1):
            res.append(0.5*(b[i]+b[i+1]))
        return res

    plt.figure(figsize=(5, 5))
    plt.grid(alpha = 0.5, linestyle = '--', linewidth = 0.2, color = 'black')
    plt.xlabel('Scores')
    plt.ylabel('Frequency')

    bbins = np.linspace(60, 101, 15) # np.geomspace(0.0001, 5500, 25)

    c, b = np.histogram(scores, bins=bbins)
    plt.plot(halven_bins(b), c/100, 'o-', markersize=4.0, markerfacecolor='none', markeredgewidth=1.0)

    # plt.xscale('log')
    # plt.savefig("results/Hist-gf(d,v)=log_p=%s.png"%i2s(p_ID), dpi=300, bbox_inches = 'tight')
    plt.show()
"""
