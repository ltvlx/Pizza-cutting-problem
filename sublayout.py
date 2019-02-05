def get_sublayout_n(pattern, x, y, wi, he, s_v, s_h):
    """
        A function that returns the sublayout number for the given input pattern key
    """
    if pattern == "left":
        if (x < s_v and x+wi-1 < s_v):
            return 1
        elif (x >= s_v and x+wi-1 >= s_v):
            return 2

    elif pattern == "upper":
        if (y < s_h and y+he-1 < s_h):
            return 1
        elif (y >= s_h and y+he-1 >= s_h):
            return 2

    elif pattern == "upper-left":
        if (x < s_v and x+wi-1 < s_v) and (y < s_h and y+he-1 < s_h):
            return 1
        elif (x >= s_v and x+wi-1 >= s_v) or (y >= s_h and y+he-1 >= s_h):
            return 2
    
    elif pattern == "upper-right":
        if (x >= s_v and x+wi-1 >= s_v) and (y < s_h and y+he-1 < s_h):
            return 1
        elif (x < s_v and x+wi-1 < s_v) or (y >= s_h and y+he-1 >= s_h):
            return 2

    elif pattern == "bottom-left":
        if (x < s_v and x+wi-1 < s_v) and (y >= s_h and y+he-1 >= s_h):
            return 1
        elif (x >= s_v and x+wi-1 >= s_v) or (y < s_h and y+he-1 < s_h):
            return 2

    elif pattern == "bottom-right":
        if (x >= s_v and x+wi-1 >= s_v) and (y >= s_h and y+he-1 >= s_h):
            return 1
        elif (x < s_v and x+wi-1 < s_v) or (y < s_h and y+he-1 < s_h):
            return 2

    elif pattern == "cross":
        if ((x >= s_v and x+wi-1 >= s_v) and (y >= s_h and y+he-1 >= s_h)) or \
            ((x < s_v and x+wi-1 < s_v) and (y < s_h and y+he-1 < s_h)):
            return 1
        elif ((x >= s_v and x+wi-1 >= s_v) and (y < s_h and y+he-1 < s_h)) or \
            ((x < s_v and x+wi-1 < s_v) and (y >= s_h and y+he-1 >= s_h)):
            return 2

    return -1



if __name__ == "__main__":
    print("Testing the 'get_sublayout_n' procedure")
    wi, he = 2, 1
    s_v, s_h = 2, 2

    test_cases = {
        0: {"left": 1,
            "upper": 1,
            "upper-left": 1,
            "upper-right": 2,
            "bottom-left": 2,
            "bottom-right": 2,
            "cross": 1},

        1: {"left": -1,
            "upper": 1,
            "upper-left": -1,
            "upper-right": -1,
            "bottom-left": 2,
            "bottom-right": 2,
            "cross": -1},

        2: {"left": 2,
            "upper": 1,
            "upper-left": 2,
            "upper-right": 1,
            "bottom-left": 2,
            "bottom-right": 2,
            "cross": 2},

        8: {"left": 1,
            "upper": 2,
            "upper-left": 2,
            "upper-right": 2,
            "bottom-left": 1,
            "bottom-right": 2,
            "cross": 2},

        9: {"left": -1,
            "upper": 2,
            "upper-left": 2,
            "upper-right": 2,
            "bottom-left": -1,
            "bottom-right": -1,
            "cross": -1},

        10: {"left": 2,
            "upper": 2,
            "upper-left": 2,
            "upper-right": 2,
            "bottom-left": 2,
            "bottom-right": 1,
            "cross": 1}
        }

    for pos in test_cases:
        y = pos // 4
        x = pos - y * 4
        for pattern in test_cases[pos]:
            assert(get_sublayout_n(pattern, x, y, wi, he, s_v, s_h) == test_cases[pos][pattern])
    
    print("Everything is correct!")
    print(test_cases[0].keys())
