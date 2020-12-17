from collections import defaultdict

inp='''
...#..#.
#..#...#
.....###
##....##
......##
........
.#......
##...#..
'''

inp = inp.strip()

D = (-1,0,1)

def solve(Dw):
    ds = [(dx,dy,dz,dw) for dx in D for dy in D for dz in D for dw in Dw if (dx,dy,dz,dw) != (0,0,0,0)]

    g = {}
    for y, row in enumerate(inp.split('\n')):
        for x, c in enumerate(row):
            if c == '#':
                g[x,y,0,0] = '#'

    for _ in range(6):
        ng = {}
        ns = defaultdict(lambda: 0)
        for (x, y, z, w), c in g.items():
            for dx, dy, dz, dw in ds:
                ns[x+dx, y+dy, z+dz, w+dw] += 1
        for (x, y, z, w), n in ns.items():
            if n == 3:
                ng[x,y,z,w] = '#'
            elif n == 2 and (x,y,z,w) in g:
                ng[x,y,z,w] = '#'
        g = ng

    return len(g)

# part 1
print(solve((0,)))
# part 2
print(solve(D))
