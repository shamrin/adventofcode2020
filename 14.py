import re
I = [l.strip() for l in open('input14.txt') if l]

# part 1
mask_or = 0
mask = ''
mask_and = int('1'*36,2)
mem = {}
for line in I:
    if line.startswith('mask = '):
        mask = line[7:]
    else:
        m = re.match(r'mem\[(\d+)\] = (\d+)', line)
        assert m
        r = int(m[2])
        r &= int(mask.replace('X', '1'), 2) # set 0s
        r |= int(mask.replace('X', '0'), 2) # set 1s
        mem[int(m[1])] = r 

print(sum(m for m in mem.values()))

# part 2
def bits(n, l):
    return list(reversed(bin(n)[2:].zfill(l)))

mask = None
mem = {}
for line in I:
    if line.startswith('mask = '):
        mask = ''.join(reversed(line[7:]))
    else:
        m = re.match(r'mem\[(\d+)\] = (\d+)', line)
        assert m
        addr, r = int(m[1]), int(m[2])
        assert mask is not None
        for count in range(2 ** mask.count('X')):
            a = bits(addr, 36)
            c = bits(count, mask.count('X'))
            for i, m in enumerate(mask):
                if m == '1':
                    a[i] = '1'
                elif m == 'X':
                    a[i] = c[mask[:i].count('X')]
            mem[int(''.join(reversed(a)), 2)] = r

print(sum(m for m in mem.values()))
