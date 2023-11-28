import src.Globals as G
import matplotlib.pyplot as plt
import src.dynamic_func

def check_cur(cur):
    """Checks if cur is available currency"""
    return cur in G.currency_list


def is_rational(x):
    """Checks if x is rational """
    point_counter = 0
    if x[0] == "." or x[-1] == ".":
        return 0
    for sym in x:
        if sym.isdigit():
            continue
        elif sym == ".":
            point_counter += 1
            if point_counter > 1:
                return 0
            continue
        else:
            return 0
    return 1
