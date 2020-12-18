import re

inputs = [line.replace(' ', '').strip() for line in open('input18.txt') if line]

class T:
    def __init__(self, I):
        self.I = I
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
        while self.I:
            if self.I[0] in '+*':
                yield 'op', self.I[0]
                self.I = self.I[1:]
            elif self.I[0] in '()':
                yield f'paren', self.I[0]
                self.I = self.I[1:]
            elif m := re.match(r'\d+', self.I):
                yield 'num', int(m.group())
                self.I = self.I[m.end():]
            else:
                raise Exception(f'Unexpected token {self.I!r}')

    def __repr__(self):
        return f'T(current={self.current}, I={self.I})'

def atom(t):
    tok, v = t.current
    if t.current == ('paren', '('):
        t.next()
        v = expr(t, 1)
        assert t.current == ('paren', ')'), repr(t.current)
        t.next()
    elif tok == 'num':
        t.next()
    else:
        raise Exception(f'Unexpected token {t.current!r} in atom')
    return v

def op(t):
    return t.current, 1 if t.current[1] == '*' else 2

def expr(t, min_prec):
    r = atom(t)
    while t.current is not None and t.current[0] == 'op':
        o, prec = op(t)
        if prec < min_prec:
            break
        t.next()
        rhs = expr(t, prec + 1) # +1 means left-assoc
        assert o[0] == 'op' and o[1] in '+*', f'unexpected op {o!r}'
        r = (r * rhs) if o[1] == '*' else (r + rhs)
    return r

print(sum(expr(T(I), 1) for i, I in enumerate(inputs)))
