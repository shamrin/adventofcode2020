from collections import Counter

inp='''
...#..#.
#..#...#
.....###
##....##
......##
........
.#......
##...#..
'''.strip()

g = {(x,y,0,0):'#' for y, row in enumerate(inp.split('\n')) for x, c in enumerate(row) if c == '#'}
D = (-1,0,1)

def add(v1, v2): return tuple(e1+e2 for e1, e2 in zip(v1,v2))
def solve(g, Dw):
    ds = [(dx,dy,dz,dw) for dx in D for dy in D for dz in D for dw in Dw if (dx,dy,dz,dw) != (0,0,0,0)]
    for _ in range(6):
        ns = Counter(add(p, d) for p in g for d in ds)
        g = {p:'#' for p, n in ns.items() if n == 3 or (n == 2 and p in g)}
    return len(g)

print(solve(g, (0,)))
print(solve(g, D))
