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

    scale = 10.0 / max(n_row, n_col)

    plt.figure(figsize=(n_row * scale, n_col * scale))
    plt.imshow(mtr, cmap='YlOrBr')
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.axis('off')

    plt.savefig("img_pizza.pdf", bbox_inches='tight', pad_inches=0.01)
    plt.close()


class Individual:
    """
    Representation of a solution to the problem (indivudual)

        layout, dict of int: int
    gene of an individual encoded as pos: k
    'pos' is the position on the pizza, [0: n_col * n_row - 1]
    k is the index of slice that has its upper left cell at this pos

        c_empty, set(int) 
    set of all cells that are empty

        s_pos_map, list[int]
    list of all cells, stores information about which slice occupies a cell;
    if cell is empty, the value in list is -1
    otherwise, it is the 'pos' from layout that occupies this cell

        n_col, n_row, int
    number of columns and rows in pizza

        L, int
    minimum number of each ingridient in a slice
    
        H, int
    maximum size of a slice
    
        slices, list[(int, int)]
    list of all possible slices with these L and H
    """
    layout = {}
    empty = set()
    s_pos_map = []
    n_col, n_row = 0, 0
    L, H = 0, 0
    slices = []

    def __init__(self, lay, slices, n_col, n_row, L, H):
        self.empty = set([i for i in range(n_row * n_col)])
        self.s_pos_map = [-1 for _ in range(n_row * n_col)]
        self.layout = dict(lay)
        self.n_col = n_col
        self.n_row = n_row
        self.L = L
        self.H = H
        self.slices = slices
        

        for pos in lay:
            k = lay[pos]
            y = pos // n_col
            x = pos - y * n_col
            wi, he = slices[k]
            for i in range(y, y+he):
                for j in range(x, x+wi):
                    c = j + i * n_col
                    self.s_pos_map[c] = pos
                    self.empty.discard(c)


    def fill_layout(self, pizza):
        """
        Procedure fills the Individual layout, which might empty or filled to some extent.
        Input layout is assumed to be correct, such that none of slices do exceed the boundary, 
        overlap with other slices, or do not satisfy the contents condition.
        """

        # can't be replaced with 'for pos in self.empty' as empty is modified in the loop
        for pos in range(self.n_row * self.n_col):
            if not pos in self.empty:
                continue

            y = pos // self.n_col
            x = pos - y * self.n_col
            if self.__isolated_cell(x, y):
                continue

            # Trying to place each type of slice in a random order
            i_slice = [i for i in range(len(self.slices))]
            random.shuffle(i_slice)
            for k in i_slice:
                wi, he = self.slices[k]
                if self.__exceeds_boundary(x, y, wi, he) or \
                    self.__collides_w_used(x, y, wi, he) or \
                    not self.__enough_contents(pizza, x, y, wi, he):
                    # Impossible to place slice k here
                    continue
                else:
                    # Placing the slice
                    self.layout[pos] = k
                    for i in range(y, y + he):
                        for j in range(x, x + wi):
                            c = j + i * self.n_col
                            self.s_pos_map[c] = pos
                            self.empty.discard(c)
                    break


    def draw_layout(self, fname="img_layout.pdf"):
        """
        Draws the image of the layout into the 'fname' as 2D colormap
        Input layout is assumed to be correct (slices are within the pizza boundaries)
        """
        mtr = np.zeros((n_row, n_col), dtype=int)

        for pos in self.layout:
            k = self.layout[pos]
            y = pos // self.n_col
            x = pos - y * self.n_col
            wi, he = self.slices[k]
            for i in range(y, y + he):
                for j in range(x, x + wi):
                    mtr[i][j] = 1
        
        scale = 10.0 / max(self.n_row, self.n_col)

        plt.figure(figsize=(n_row * scale, n_col * scale))
        plt.imshow(mtr, cmap='YlOrBr_r')
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.axis('off')

        plt.savefig(fname, bbox_inches='tight', pad_inches=0.01)    
        plt.close()


    def mutate(self, pizza):
        """
        Mutate individual:
        1. Pick a random empty cell 'pos_start'
        2. Select the cluster of empty cells around 'pos_start'
        3. Remove all slices that are adjacent to the cluster
        4. Fill the layout again
        """
        pos_start = random.choice(tuple(self.empty))

        _, to_remove = self.__get_adjacent(pos_start, visited=set(), to_remove=set())

        for pos in to_remove:
            k = self.layout.pop(pos)

            y = pos // self.n_col
            x = pos - y * self.n_col
            wi, he = self.slices[k]
            for i in range(y, y + he):
                for j in range(x, x + wi):
                    c = j + i * self.n_col
                    self.s_pos_map[c] = -1
                    self.empty.add(c)

        self.fill_layout(pizza)


    def efficiency(self):
        return 100 * (1 - len(self.empty) / self.n_row / self.n_col)

    def score(self):
        return self.n_col * self.n_row - len(self.empty)

    ###########################################################################

    def __isolated_cell(self, x, y):
        """
        Checks if there is a border or a filled cell to the left of (x,y) AND down the (x,y).
        If so, then the cell is isolated and nothing would fit there.
        """
        if ((x+1 >= self.n_col) or not (x+1 + y*self.n_col) in self.empty) and \
            ((y+1 >= self.n_row) or not (x + (y+1)*self.n_col) in self.empty):
            return True
        return False


    def __exceeds_boundary(self, x, y, wi, he):
        """
        Checks, if the slice (wi, he) placed at (x, y) would exceed one of the pizza boundaries
        """
        return (x + wi > self.n_col) or (y + he > self.n_row)


    def __collides_w_used(self, x, y, wi, he):
        """
        Checks, if the slice (wi, he) placed at (x, y) would overlap with one of the non-empty pizza cells
        """
        for i in range(y, y + he):
            for j in range(x, x + wi):
                c = j + i * self.n_col
                if not c in self.empty:
                    return True
        return False


    def __enough_contents(self, pizza, x, y, wi, he):
        """
        Checks, if the slice (wi, he) placed at (x, y) would have enough of M and T contents
        """
        T = 0
        M = 0
        for i in range(y, y + he):
            for j in range(x, x + wi):
                v = pizza[i][j]
                if v == 'T':
                    T += 1
                else:
                    M += 1
        return (T >= self.L) and (M >= self.L)


    def __get_adjacent(self, pos, visited, to_remove):
        """
        Finds all slices that are adjacent to the block of empty cells with the beginning at 'pos'
        
        visited, set(int)
            set of cells that have already been visited by the procedure
        
        to_remove, set(int)
            set of adjacent slices positions, that will be removed during the mutation
        """
        visited.add(pos)

        if not pos in self.empty:
            to_remove.add(self.s_pos_map[pos])
            return visited, to_remove
        else:
            
            possible_moves = []
            for p in [pos+1, pos-1]:
                if pos // self.n_col == p // self.n_col:
                    possible_moves.append(p)
            for p in [pos + self.n_col, pos - self.n_col]:
                if not (p // self.n_col  in [-1, self.n_row]):
                        possible_moves.append(p)

            for p in possible_moves:
                if not p in visited:
                    visited, to_remove = self.__get_adjacent(p, visited, to_remove)
            
            return visited, to_remove


    def __str__(self):
        return "<%6.3f%%, %d>"%(self.efficiency(), self.score())


def recombine(ind_A, ind_B, pizza):
    """
    Creates two new indivuduals based on parents ind_A and ind_B

    Scheme:
    1. get random vertical and horizontal (s_v, s_h) lines that split both individuals in four non-empty sectors:
         c_v
        1x|2xxx
        xx|xxxx
     c_h--+----
        3x|4xxx
        xx|xxxx
    
    2. For each individual, create random sub-layouts that strictly fall into each of four sectors:
        ind_A_1, ind_A_2, ind_A_3, ind_A_4, ind_B_1, ...

    3. Randomly choose a pattern for rotation:
        [1, 2, 3, 4, 12, 13, 14]
        others are not necessary, because pattern 123 == 4

    4. Create new individuals by merging according to the chosen pattern:
        e.g. pattern = 12
        ind_C = ind_A_1 + ind_A_2 + ind_B_3 + ind_B_4
        ind_D = ind_B_1 + ind_B_2 + ind_A_3 + ind_A_4

    """




if __name__ == "__main__":
    pizza, n_row, n_col, L, H = read_setup("input/c_medium.in") # a_example  b_small  c_medium  d_big
    slices = generate_possible_slices(L, H)
    # print("Max score is %d"%(n_col * n_row))
    # for i in range(len(slices)):
    #     print(i, slices[i])
    draw_pizza(pizza)

    A = Individual({}, slices, n_col, n_row, L, H)
    # A.fill_layout(pizza)
    print(A)

    recombine(A, A, pizza)

    # A.mutate(pizza)
    # print("After a mutation:")
    # print(A)
    # # A.draw_layout()


