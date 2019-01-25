import random
import codecs
import numpy as np
import matplotlib.pyplot as plt
# random.seed(0)


def read_setup(fname):
    """
    Reading the setup from the input file 'fname'.
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


def generate_possible_slices(_L, _H):
    """
    Generates a list of all possible slices based on _L and _H.
    Each slice is encoded as (l, h) - it's length and height, respectively.
    """
    n_min = 2 * _L
    n_max = _H

    slices = []
    for h in range(1, n_max+1):
        for l in range(max(1, n_min // h), n_max + 1):
            if h*l > n_max:
                break
            slices.append((l,h))

    return slices


def draw_pizza(pizza):
    """
    Draws the image of pizza into the "img_pizza.pdf" as 2D colormap
    """
    n_row = len(pizza)
    n_col = len(pizza[0])

    mtr = np.zeros((n_row, n_col), dtype=int)
    for i in range(n_row):
        row = pizza[i]
        _row = row.replace('T', '1')
        _row = _row.replace('M', '0')
        _row = list(map(int, list(_row)))
        mtr[i] = np.array(_row)

    scale = 8 / max(n_row, n_col)
    # print((n_row * scale, n_col * scale))

    plt.figure(figsize=(n_row * scale, n_col * scale))
    plt.imshow(mtr, cmap='YlOrBr')
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.axis('off')

    plt.savefig("img_pizza.pdf", bbox_inches='tight', pad_inches=0.01)
    plt.close()
    # plt.show()


def draw_layout(layout, slices, n_row, n_col):
    """
    Draws the image of the layout into the "img_layout.pdf" as 2D colormap
    Input layout is assumed to be correct (slices are within the pizza boundaries)
    """
    mtr = np.zeros((n_row, n_col), dtype=int)

    for pos, k in layout:
        y = pos // n_col
        x = pos - y * n_col
        l, h = slices[k]
        for i in range(y, y+h):
            for j in range(x, x+l):
                mtr[i][j] = 1
    
    scale = 8 / max(n_row, n_col)
    # print((n_row * scale, n_col * scale))

    plt.figure(figsize=(n_row * scale, n_col * scale))
    plt.imshow(mtr, cmap='YlOrBr_r')
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.axis('off')

    plt.savefig("img_layout.pdf", bbox_inches='tight', pad_inches=0.01)    
    # plt.show()
    plt.close()



def isolated_cell(c_used, x, y, n_row, n_col):
    """
    Checks if there is a border or a filled cell to the left or down the (x,y).
    If so, then the cell is isolated and nothing would fit there.
    """
    if ((x+1 >= n_col) or bool(c_used[x+1 + y * n_col])) and ((y+1 >= n_row) or bool(c_used[x + (y+1) * n_col])):
        return True
    return False


def exceeds_boundary(x, y, l, h, n_row, n_col):
    """
    Checks, if the slice (l, h) placed at (x, y) would exceed one of the pizza boundaries
    """
    return (x+l > n_col) or (y+h > n_row)


def collides_w_used(c_used, x, y, l, h):
    """
    Checks, if the slice (l, h) placed at (x, y) would overlap with one of the used pizza cells
    """
    for i in range(y, y+h):
        for j in range(x, x+l):
            c = j + i * n_col
            if c_used[c]:
                return True
    return False


def enough_contents(pizza, _L, x, y, l, h):
    """
    Checks, if the slice (l, h) placed at (x, y) would have enough of M and T contents
    """
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


def fill_empty_used(layout, slices, n_col):
    """
    The procedure fills lists 'c_empty' and 'c_used' based on the input layout
    """
    c_empty = [1 for _ in range(n_row * n_col)]
    c_used = [0 for _ in range(n_row * n_col)]

    for pos, k in layout:
        y = pos // n_col
        x = pos - y * n_col
        l, h = slices[k]
        for i in range(y, y+h):
            for j in range(x, x+l):
                c = j + i * n_col
                c_used[c] = 1
                c_empty[c] = 0

    return c_empty, c_used


def generate_layout(layout, slices, n_col, n_row):
    """
    Procedure generates a new layout of slices based on the one in input.
    Input layout might empty or filled to some extent.
    Input layout is assumed to be correct, such that none of slices do exceed the boundary, overlap with other slices, or do not satisfy the contents condition.

    layout  --  gene of an individual encoded as tuples (pos, k)
                pos is the position on the pizza, 0 <= pos <= n_col * n_row - 1
                k is the index of slice that has its upper left cell at this pos


    c_empty --  cells that are empty and a slice can use them
    c_used  --  cells that are occupied by either a slice, or by randomly assigned unused cell
                it might be necessary in future to have a different list for unused cells
    """

    c_empty, c_used = fill_empty_used(layout, slices, n_col)
    
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
        if isolated_cell(c_used, x, y, n_row, n_col):
            # cell 'pos' is isolated. Nothing can be fitted here, skipping.
            # print(" - pos=%d is isolated. Skipping it."%pos)
            continue

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



pizza, n_row, n_col, _L, _H = read_setup("input/c_medium.in") # 
slices = generate_possible_slices(_L, _H)

# print("Slices: ", slices)
draw_pizza(pizza)

for i in range(len(slices)):
    print(i, slices[i])


print("Max score is %d"%(n_col * n_row))
# layout = [(0, 4), (1, 8), (2, 3), (10, 0), (12, 8), (13, 4), (16, 0), (18, 6), (23, 0)]
layout = []

c_empty, c_used, layout = generate_layout(layout, slices, n_col, n_row)
draw_layout(layout, slices, n_row, n_col)

        
efficiency = 100 * (1 - sum(c_empty) / n_row / n_col)
print("The efficiency of the created layout = %5.2f%%; score is %d"%(efficiency, sum(c_used)))
# print(layout)



