import sympy


def freqstate(W, s):
    w = sympy.Symbol('w')
    W = sympy.simplify(W)
    n, d = sympy.fraction(W)
    D = d.subs(d, (s, w*1j))
    foo = sympy.lambdify(w, D, 'numpy')
    return foo
