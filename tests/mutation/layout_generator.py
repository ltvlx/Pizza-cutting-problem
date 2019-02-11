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


def draw_layout(layout, slices, n_row, n_col, fname="img_layout.pdf"):
    """
    Draws the image of the layout into the "img_layout.pdf" as 2D colormap
    Input layout is assumed to be correct (slices are within the pizza boundaries)
    """
    mtr = np.zeros((n_row, n_col), dtype=int)

    for pos in layout:
        k = layout[pos]
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

    plt.savefig(fname, bbox_inches='tight', pad_inches=0.01)    
    # plt.show()
    plt.close()


def isolated_cell(c_empty, x, y, n_row, n_col):
    """
    Checks if there is a border or a filled cell to the left of (x,y) AND down the (x,y).
    If so, then the cell is isolated and nothing would fit there.
    """
    if ((x+1 >= n_col) or not (x+1 + y * n_col) in c_empty) and ((y+1 >= n_row) or not (x + (y+1) * n_col) in c_empty):
        return True
    return False


def exceeds_boundary(x, y, l, h, n_col, n_row):
    """
    Checks, if the slice (l, h) placed at (x, y) would exceed one of the pizza boundaries
    """
    return (x+l > n_col) or (y+h > n_row)


def collides_w_used(c_empty, x, y, l, h, n_col):
    """
    Checks, if the slice (l, h) placed at (x, y) would overlap with one of the non-empty pizza cells
    """
    for i in range(y, y+h):
        for j in range(x, x+l):
            c = j + i * n_col
            if not c in c_empty:
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


def fill_empty_used(layout, slices, n_col, n_row):
    """
    The procedure fills lists 'c_empty' and 'c_slice' based on the input layout
    """
    c_empty = set([i for i in range(n_row * n_col)])
    c_slice = [-1 for _ in range(n_row * n_col)]

    for pos in layout:
        k = layout[pos]
        y = pos // n_col
        x = pos - y * n_col
        l, h = slices[k]
        for i in range(y, y+h):
            for j in range(x, x+l):
                c = j + i * n_col
                c_slice[c] = pos
                c_empty.discard(c)

    return c_empty, c_slice


def generate_layout(pizza, _L, layout, slices, n_col, n_row):
    """
    Procedure generates a new layout of slices based on the one in input.
    Input layout might empty or filled to some extent.
    Input layout is assumed to be correct, such that none of slices do exceed the boundary, overlap with other slices, or do not satisfy the contents condition.

    layout, dict of int: int
        gene of an individual encoded as pos: k
        pos is the position on the pizza, 0 <= pos <= n_col * n_row - 1
        k is the index of slice that has its upper left cell at this pos

    c_empty, set(int) 
        set of all cells that are empty

    c_slice, list[int]
        list of all pizza cells; if cell is not empty, element is the 'pos' from layout that occupies this cell; otherwise, -1
    """

    c_empty, c_slice = fill_empty_used(layout, slices, n_col, n_row)
    
    for pos in range(n_row * n_col):
        if not pos in c_empty:
            continue
        
        y = pos // n_col
        x = pos - y * n_col
        if isolated_cell(c_empty, x, y, n_row, n_col):
            # cell 'pos' is isolated. Nothing can be fitted here, skipping.
            # print(" - pos=%d is isolated. Skipping it."%pos)
            continue

        # Trying to place each type of slice in a random order
        i_slice = [i for i in range(len(slices))]
        random.shuffle(i_slice)
        for k in i_slice:
            l, h = slices[k]
            if exceeds_boundary(x, y, l, h, n_col, n_row) or collides_w_used(c_empty, x, y, l, h, n_col) or not enough_contents(pizza, _L, x, y, l, h):
                # Impossible to place slice k here
                continue
            else:
                # Placing the slice
                layout[pos] = k
                for i in range(y, y+h):
                    for j in range(x, x+l):
                        c = j + i * n_col
                        c_slice[c] = pos
                        c_empty.discard(c)
                break
    return c_empty, c_slice, layout


if __name__ == "__main__":
    pizza, n_row, n_col, _L, _H = read_setup("input/c_medium.in") # a_example  b_small  c_medium  d_big
    slices = generate_possible_slices(_L, _H)

    # for i in range(len(slices)):
    #     print(i, slices[i])

    # print("Max score is %d"%(n_col * n_row))

    # layout = {}
    # c_empty, c_slice, layout = generate_layout(pizza, _L, layout, slices, n_col, n_row)
            
    # efficiency = 100 * (1 - len(c_empty) / n_row / n_col)
    # print("The efficiency of the created layout = %5.2f%%; score is %d"%(efficiency, n_col * n_row - len(c_empty)))
    # # print(layout)
    # # print(c_empty)

    # draw_pizza(pizza)
    # draw_layout(layout, slices, n_row, n_col, "img_layout_initial.pdf")
    
    
    import json
    with codecs.open("medium_98-27.json", "r") as fin:
        data = json.load(fin)
    layout = {}
    for p, k in data.items():
        print(p,k)
        layout[int(p)] = k
    
    c_empty, c_slice = fill_empty_used(layout, slices, n_col, n_row)

    efficiency = 100 * (1 - len(c_empty) / n_row / n_col)
    print("The efficiency of the created layout = %5.2f%%; score is %d"%(efficiency, n_col * n_row - len(c_empty)))

    draw_layout(layout, slices, n_row, n_col, "img_layout-init-0.pdf")
    fx = []
    fy = []
    import mutations as mtns


    print("Now mutating:")
    for i in range(100000):
        _lay = dict(layout)
        _empty, _slice = set(c_empty), list(c_slice)
        if not c_empty:
            print("Maximum efficiency achieved!")
            print(layout)
            break

        _empty, _slice, _lay = mtns.mutate(pizza, _L, _lay, slices, _empty, _slice, n_col, n_row)
        _eff = 100 * (1 - len(_empty) / n_row / n_col)
        if _eff > efficiency:
            print("#%d,  %5.2f%% --> %5.2f%%"%(i, efficiency, _eff))
            layout = _lay
            efficiency = _eff
            c_slice = _slice
            c_empty = _empty

            fx.append(i)
            fy.append(efficiency)


    with codecs.open("medium_init-1.json", 'w') as fout:
        json.dump(layout, fout, sort_keys=True)

    with codecs.open("convergence.json", 'w') as fout:
        json.dump({"iterations": fx, "efficiency": fy}, fout)
    draw_layout(_lay, slices, n_row, n_col, "img_layout_muta-1.pdf")
