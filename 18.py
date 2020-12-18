import re

inputs = [line.replace(' ', '').strip() for line in open('input18.txt') if line]

class peekable:
    def __init__(self, it):
        self.it = iter(it)
        self.cache = []

    def peek(self):
        if not self.cache:
            try:
                self.cache.append(next(self.it))
            except StopIteration:
                return None
        return self.cache[-1]

    def __next__(self):
        if self.cache:
            return self.cache.pop()
        return next(self.it)

    def __iter__(self):
        return self

def tokens(input, precedence):
    input = input.strip().replace(' ', '')
    i = 0
    while i < len(input):
        c = input[i]
        if c in '+*':
            yield 'op', c, precedence[c]
            i += 1
        elif c in '(':
            yield f'lparen', None
            i += 1
        elif c in ')':
            yield f'rparen', None
            i += 1
        elif m := re.match(r'\d+', input[i:]):
            yield 'num', int(m.group())
            i += m.end()
        else:
            raise Exception(f'Unexpected token {input[i:]!r}')

def atom(t):
    tok, v = t.peek()
    if tok == 'lparen':
        next(t)
        v = expr(t, 1)
        assert t.peek()[0] == 'rparen', repr(t.peek())
        next(t)
    elif tok == 'num':
        next(t)
    else:
        raise Exception(f'Unexpected token {t.peek()!r}')
    return v

def expr(t, min_prec):
    r = atom(t)
    while t.peek() is not None and t.peek()[0] == 'op':
        o, prec = t.peek()[1:]
        if prec < min_prec:
            break
        next(t)
        rhs = expr(t, prec + 1) # +1 means left-assoc
        assert o in '+*', f'unexpected op {o!r}'
        r = (r * rhs) if o == '*' else (r + rhs)
    return r

# print(expr(peekable(tokens('1 + 2 * 3 + 4 * 5 + 6', {'+': 1, '*': 1})), 1))

for precedence in [{'*':1,'+':1}, {'*':1,'+':2}, {'*':2,'+':1}]:
    print(sum(expr(peekable(tokens(I, precedence)), 1) for I in inputs))
