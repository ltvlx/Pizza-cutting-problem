import random
import codecs
import numpy as np
import matplotlib.pyplot as plt
import json
from sublayout import get_sublayout_n
# random.seed()


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

            layout, dict of (int, int): int
        gene of an individual encoded as (x, y): k
        (x, y) is the position on the pizza, ([0:n_col], [n_row])
        k is the index of slice that has its upper left cell at this pos

            c_empty, set((int, int)) 
        set of all (x,y) cells that are empty

            s_pos_map, dict of (int, int)
        dict of all used cells, stores information about which slice occupies a cell;
        if a cell is empty, it is not in this dict
        otherwise, it is the (x,y) from layout that occupies this cell

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
    slice_map = {}
    n_col, n_row = 0, 0
    L, H = 0, 0
    slices = []

    def __init__(self, lay, slices, n_col, n_row, L, H):
        self.empty = set([(x, y) for x in range(n_col) for y in range(n_row)])
        self.layout = dict(lay)
        self.n_col = n_col
        self.n_row = n_row
        self.L = L
        self.H = H
        self.slices = slices

        for (x, y) in self.layout:
            k = self.layout[(x, y)]
            wi, he = self.slices[k]
            for j in range(y, y+he):
                for i in range(x, x+wi):
                    self.slice_map[(i, j)] = (x, y)
                    self.empty.discard((i, j))


    def fill_layout(self, pizza):
        """
            Procedure fills the Individual layout, which might empty or filled to some extent.
            Input layout is assumed to be correct, such that none of slices do exceed the boundary, 
            overlap with other slices, or do not satisfy the contents condition.
        """

        for y in range(self.n_row):
            for x in range(self.n_col):
                if not (x,y) in self.empty or self.__isolated_cell(x, y):
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
                        self.layout[(x,y)] = k
                        for j in range(y, y + he):
                            for i in range(x, x + wi):
                                self.slice_map[(i, j)] = (x, y)
                                self.empty.remove((i, j))
                                # self.empty.discard(c)
                        break


    def draw_layout(self, fname="img_layout.pdf"):
        """
            Draws the image of the layout into the 'fname' as 2D colormap
            Input layout is assumed to be correct (slices are within the pizza boundaries)
        """
        mtr = np.zeros((self.n_row, self.n_col), dtype=int)

        for (x, y), k in self.layout.items():
            wi, he = self.slices[k]
            for i in range(y, y + he):
                for j in range(x, x + wi):
                    mtr[i][j] = 1
        
        scale = 10.0 / max(self.n_row, self.n_col)

        plt.figure(figsize=(self.n_row * scale, self.n_col * scale))
        plt.imshow(mtr, cmap='YlOrBr_r')
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.axis('off')

        plt.savefig(fname, bbox_inches='tight', pad_inches=0.01)    
        plt.close()


    def mutate(self, pizza):
        """
            Mutate individual:
            1. Pick a random empty cell (sx, sy)
            2. Select the cluster of empty cells around (sx, sy)
            3. Remove all slices that are adjacent to the cluster
            4. Fill the layout again
        """
        if not self.empty:
            return

        sx, sy = random.choice(tuple(self.empty))

        _, to_remove = self.__get_adjacent(sx, sy, visited=set(), to_remove=set())

        for (x, y) in to_remove:
            k = self.layout.pop((x, y))

            wi, he = self.slices[k]
            for j in range(y, y + he):
                for i in range(x, x + wi):
                    self.slice_map.pop((i, j))
                    self.empty.add((i, j))

        self.fill_layout(pizza)


    def recombine(self, other, pizza):
        """
            Creates two new indivuduals based on parents 'self' and 'other'

            Scheme:
            1. get random vertical and horizontal (s_x, s_y) lines that split both individuals in four non-empty sectors:
                s_x
                xx|xxxx
                xx|xxxx
            s_y --+----
                xx|xxxx
                xx|xxxx
            
            2. Randomly choose a pattern for swap, that defines which two zones will be swapped between 'self' and 'other'
            left    upper    cross
                █░      ██       █░
                █░      ░░       ░█
            upper-left      upper-right     bottom-left     bottom-right
                █░              ░█              ░░              ░░
                ░░              ░░              █░              ░█

            3. For 'self' and 'other', create sub-layouts A_1, A_2, B_1, and B_2 that strictly fall into the pattern zones.

            4. Create new individuals by swapping the sub-zones:
                C = A_1 + B_2
                D = A_2 + B_1
        """
        s_x = random.randint(1, self.n_col-1)
        s_y = random.randint(1, self.n_row-1)

        pattern = random.choice(['left', 'upper', 'upper-left', 'upper-right', 'bottom-left', 'bottom-right', 'cross'])
        A_1, A_2 = {}, {}
        for (x, y), k in self.layout.items():
            wi, he = self.slices[k]
            n = get_sublayout_n(pattern, x, y, wi, he, s_x, s_y)
            if n == 1:
                A_1[(x,y)] = k
            elif n == 2:
                A_2[(x,y)] = k

        B_1, B_2 = {}, {}
        for (x,y), k in other.layout.items():
            wi, he = self.slices[k]
            n = get_sublayout_n(pattern, x, y, wi, he, s_x, s_y)
            if n == 1:
                B_1[(x,y)] = k
            elif n == 2:
                B_2[(x,y)] = k

        C = Individual({**A_1, **B_2}, self.slices, self.n_col, self.n_row, self.L, self.H)
        C.fill_layout(pizza)
        D = Individual({**A_2, **B_1}, self.slices, self.n_col, self.n_row, self.L, self.H)
        D.fill_layout(pizza)
        return C, D


    def efficiency(self):
        return 100 * (1 - len(self.empty) / self.n_row / self.n_col)


    def score(self):
        return self.n_col * self.n_row - len(self.empty)


    def copy(self):
        return Individual(self.layout, self.slices, self.n_col, self.n_row, self.L, self.H)


    def dump_layout(self, fname):
        with codecs.open(fname, 'w') as fout:
            json.dump(self.layout, fout)


    def check_correctness(self, pizza):
        """
            Checks the correctness of current layout
        """
        self.empty = set([i for i in range(self.n_row * self.n_col)])
        for (x,y), k in self.layout.items():
            wi, he = self.slices[k]

            if self.__exceeds_boundary(x, y, wi, he) or \
                self.__collides_w_used(x, y, wi, he) or \
                not self.__enough_contents(pizza, x, y, wi, he):
                return False
            else:
                for j in range(y, y + he):
                    for i in range(x, x + wi):
                        if not (i,j) in self.empty:
                            return False
                        self.empty.remove((x,y))
        return True


    ###########################################################################

    def __isolated_cell(self, x, y):
        """
            Checks if there is a border or a filled cell to the left of (x,y) AND down the (x,y).
            If so, then the cell is isolated and nothing would fit there.
        """
        if ((x+1 >= self.n_col) or not (x+1, y) in self.empty) and \
            ((y+1 >= self.n_row) or not (x, y+1) in self.empty):
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
        for j in range(y, y + he):
            for i in range(x, x + wi):
                if not (i, j) in self.empty:
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


    def __get_adjacent(self, x, y, visited, to_remove):
        """
            Finds all slices that are adjacent to the block of empty cells with the beginning at 'pos'
            
            visited, set(int)
                set of cells that have already been visited by the procedure
            
            to_remove, set(int)
                set of adjacent slices positions, that will be removed during the mutation
        """
        visited.add((x,y))

        if not (x,y) in self.empty:
            to_remove.add(self.slice_map[(x,y)])
            return visited, to_remove

        else:
            possible_moves = []
            if x+1 < self.n_col:
                possible_moves.append((x+1,y))
            if x-1 >= 0:
                possible_moves.append((x-1,y))
            if y+1 < self.n_row:
                possible_moves.append((x,y+1))
            if y-1 >= 0:
                possible_moves.append((x,y-1))

            for (x,y) in possible_moves:
                if not (x, y) in visited:
                    visited, to_remove = self.__get_adjacent(x, y, visited, to_remove)
            return visited, to_remove


    def __str__(self):
        return "<%6.3f%%, %d>"%(self.efficiency(), self.score())

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.score() < other.score()

    def __le__(self, other):
        return self.score() <= other.score()

    def __gt__(self, other):
        return self.score() > other.score()

    def __ge__(self, other):
        return self.score() >= other.score()



if __name__ == "__main__":
    pizza, n_row, n_col, L, H = read_setup("input/c_medium.in") # a_example  b_small  c_medium  d_big
    slices = generate_possible_slices(L, H)
    # print("Max score is %d"%(n_col * n_row))
    # for i in range(len(slices)):
    #     print(i, slices[i])
    draw_pizza(pizza)

    A = Individual({}, slices, n_col, n_row, L, H)
    A.fill_layout(pizza)
    print(A)

    # B = Individual({}, slices, n_col, n_row, L, H)
    # B.fill_layout(pizza)
    # print(B)

    # C, D = A.recombine(B, pizza)
    # print(C, D)
    # A.mutate(pizza)
    # print("After a mutation:")
    # print(i, A)
    # A.draw_layout()

    # scores = []
    # for i in range(10):
    #     print(i)
    #     C, D = A.recombine(B, pizza)
    #     scores.append(C.efficiency())
    #     scores.append(D.efficiency())
    


    # plt.figure(figsize=(6, 6))

    # plt.hist(scores, bins=20)
    # plt.plot([A.efficiency()]*2, [0, 10], c='black')
    # plt.plot([B.efficiency()]*2, [0, 10], c='black')

    # plt.savefig("recombination_test.pdf", bbox_inches='tight')
    # plt.savefig("recombination_test.png", bbox_inches='tight', dpi=300)
    # plt.show()

