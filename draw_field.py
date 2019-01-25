import random
import codecs
import numpy as np
import matplotlib.pyplot as plt


def read_setup(fname):
    with codecs.open(fname, 'r') as fin:
        n_row, n_col, L, H = list(map(int, fin.readline().split()))

        pizza = []
        for _ in range(n_row):
            line = fin.readline().strip()
            pizza.append(line)

    return pizza, n_row, n_col, L, H


# pizza, n_row, n_col, _L, _H = read_setup("a_example.in")
# pizza, n_row, n_col, _L, _H = read_setup("b_small.in")
pizza, n_row, n_col, _L, _H = read_setup("c_medium.in")
# pizza, n_row, n_col, _L, _H = read_setup("d_big.in")



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

plt.savefig("pizza_image.pdf", bbox_inches = 'tight')
# plt.show()

