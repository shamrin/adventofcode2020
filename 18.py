import re

inputs = [line.replace(' ', '').strip() for line in open('input18.txt') if line]

class T:
    def __init__(self, input, precedence):
        self.input = input
        self.i = 0
        self.precedence = precedence
        self.current = None
        self.gen = self._gen()
        self.next()

    def next(self):
        try:
            self.current = next(self.gen)
        except StopIteration:
            self.current = None
        return self.current

    def _gen(self):
        while self.i < len(self.input):
            c = self.input[self.i]
            if c in '+*':
                yield 'op', c, self.precedence[c]
                self.i += 1
            elif c in '()':
                yield f'paren', c
                self.i += 1
            elif m := re.match(r'\d+', self.input[self.i:]):
                yield 'num', int(m.group())
                self.i += m.end()
            else:
                raise Exception(f'Unexpected token {self.input[self.i:]!r}')

    def __repr__(self):
        return f'T(current={self.current}, I={self.input[self.i:]})'

def atom(t):
    tok, v = t.current
    if (tok, v) == ('paren', '('):
        t.next()
        v = expr(t, 1)
        assert t.current == ('paren', ')'), repr(t.current)
        t.next()
    elif tok == 'num':
        t.next()
    else:
        raise Exception(f'Unexpected token {t.current!r} in atom: {t.I!r}')
    return v

def op(t):
    return t.current, 1 if t.current[1] == '*' else 2

def expr(t, min_prec):
    r = atom(t)
    while t.current is not None and t.current[0] == 'op':
        o, prec = t.current[1:]
        if prec < min_prec:
            break
        t.next()
        rhs = expr(t, prec + 1) # +1 means left-assoc
        assert o in '+*', f'unexpected op {o!r}'
        r = (r * rhs) if o == '*' else (r + rhs)
    return r

print(sum(expr(T(I, {'*': 1, '+': 1}), 1) for I in inputs))
print(sum(expr(T(I, {'*': 1, '+': 2}), 1) for I in inputs))
print(sum(expr(T(I, {'*': 2, '+': 1}), 1) for I in inputs))
