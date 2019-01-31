import random
from layout_generator import generate_layout

def get_adjacent(pos, visited, to_remove, c_empty, c_slice, n_col, n_row):
    visited.add(pos)

    if not pos in c_empty:
        to_remove.add(c_slice[pos])
        return visited, to_remove
    else:
        
        possible_moves = []
        for p in [pos+1, pos-1]:
            if pos // n_col == p // n_col:
                possible_moves.append(p)
        for p in [pos + n_col, pos - n_col]:
            if not (p // n_col  in [-1, n_row]):
                    possible_moves.append(p)

        for p in possible_moves:
            if not p in visited:
                visited, to_remove = get_adjacent(p, visited, to_remove, c_empty, c_slice, n_col, n_row)
        
        return visited, to_remove


def mutate(pizza, _L, layout, slices, c_empty, c_slice, n_col, n_row):
    empty_pos = random.choice(tuple(c_empty))

    visited, to_remove = get_adjacent(empty_pos, set(), set(), c_empty, c_slice, n_col, n_row)

    for pos in to_remove:
        k = layout.pop(pos)

        y = pos // n_col
        x = pos - y * n_col
        l, h = slices[k]
        for i in range(y, y+h):
            for j in range(x, x+l):
                c = j + i * n_col
                c_slice[c] = -1
                c_empty.add(c)
    visited.clear()
    to_remove.clear()


    c_empty, c_slice, layout = generate_layout(pizza, _L, layout, slices, n_col, n_row)

    return c_empty, c_slice, layout



# layout = {0: 7, 1: 2, 5: 2, 9: 7, 10: 6, 12: 2, 16: 8, 17: 5, 19: 7, 23: 0, 25: 5, 34: 4, 35: 4, 39: 5, 43: 6, 61: 1}
# scores = []
# for i in range(10000):
#     ll = dict(layout)
#     c_empty, c_slice = lg.fill_empty_used(ll, slices, n_col)

#     visited, to_remove = get_adjacent(44, set(), set(), c_empty, c_slice, n_col, n_row)
#     for pos in to_remove:
#         layout.pop(pos)
#     c_empty, c_slice, ll = generate_layout(ll, slices, n_col, n_row)
#     _e = 100 * (1 - sum(c_empty) / n_row / n_col)
#     scores.append(_e)


# def halven_bins(b):
#     res = []
#     for i in range(len(b)-1):
#         res.append(0.5*(b[i]+b[i+1]))
#     return res

# print(max(scores))

# plt.figure(figsize=(5, 5))
# plt.grid(alpha = 0.5, linestyle = '--', linewidth = 0.2, color = 'black')

# bbins = np.linspace(50, 100, 20)
# # plt.hist(scores,bins=bbins)
# c, b = np.histogram(scores, bins=bbins)
# plt.plot(halven_bins(b), c/100, 'o-', markersize=4.0, markerfacecolor='none', markeredgewidth=1.0)

# plt.plot([efficiency]*2, [0, 40], '-', c="black")
# plt.plot([np.mean(scores)]*2, [0, 40], '-', c="red")

# plt.show()




# print()



