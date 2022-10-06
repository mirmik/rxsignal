import numpy
from rxsignal.observable import feedback_subject
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


def dynsystem(g, A, B, step, init=None):
    Ad, Bd = matrix_discretization2(A, B, step)
    if init is None:
        init = numpy.zeros(len(B))

    x0 = feedback_subject()
    x1 = x0.map(lambda a: numpy.matmul(Ad, a)) + g.map(lambda g: Bd*g)
    x1.subscribe(lambda a: x0.on_next(a))
    x0.on_next(init)
    return x1


def dynsystem2(g, A, B, C, D, step, init=None):
    Ad, Bd, Cd, Dd = matrix_discretization4(A, B, C, D, step)

    if init is None:
        init = numpy.zeros(len(B))

    x0 = feedback_subject()
    x1 = numpy.matmul(Ad, x0) + numpy.matmul(Bd, g)
    y1 = numpy.matmul(Cd, x0) + numpy.matmul(Dd, g)
    x1.subscribe(lambda a: x0.on_next(a))
    x0.on_next(init)
    return y1
