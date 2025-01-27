from itertools import *

def f(x, y, z, w):
    return w and (y == (z <= (x and y)))

tabl = [(0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 1), (1, 0, 0, 1)]

for a in product([0, 1], repeat=5):
    t = [(a[0], 0, 0, a[1]), (1, a[2], 1, 0), (a[3], a[4], 1, 0)]
    if len(t) == len(set(t)):
        if f(t[0], t[1], t[2]):
            print(t)