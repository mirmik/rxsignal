import numpy
from rxsignal.observable import FeedbackSubject
from scipy import linalg
import numpy as np


def matrix_discretization2(A, B, Step):
    _A = linalg.expm(A * Step)
    _B = linalg.inv(A).dot((_A - np.identity(A.shape[0])).dot(B))
    return (_A, _B)


def matrix_discretization4(A, B, C, D, Step):
    _A = linalg.expm(A * Step)
    _B = linalg.inv(A).dot((_A - np.identity(A.shape[0])).dot(B))
    _C = C
    _D = D
    return (_A, _B, _C, _D)


class DynamicSystem:
    def __init__(self, g, A, B, step, C=None, D=None, init=None):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.g = g
        self.step = step
        self.init = init

        if self.C is not None:
            self._Ad, self._Bd, self._Cd, self._Dd = matrix_discretization4(A, B, C, D, step)
            self._out = self.dynsystem2(g, self._Ad, self._Bd, self._Cd, self._Dd, step, init)
        else:
            self._Ad, self._Bd = matrix_discretization2(A, B, step)
            self._out = self.dynsystem(g, self._Ad, self._Bd, step, init)

    def dynsystem(self, g, Ad, Bd, step, init=None):
        if init is None:
            init = numpy.zeros(len(B))

        x0 = FeedbackSubject()
        x1 = x0.map(lambda a: numpy.matmul(Ad, a)) + g.map(lambda g: Bd*g)
        x1.subscribe(lambda a: x0.on_next(a))
        x0.on_next(init)
        return x1

    def dynsystem2(self, g, Ad, Bd, Cd, Dd, step, init=None):
        if init is None:
            init = numpy.zeros(len(B))

        x0 = FeedbackSubject()
        x1 = numpy.matmul(Ad, x0) + numpy.matmul(Bd, g)
        y1 = numpy.matmul(Cd, x0) + numpy.matmul(Dd, g)
        x1.subscribe(lambda a: x0.on_next(a))
        x0.on_next(init)
        return y1

    def out(self):
        return self._out
