from rxsignal.observable import FeedbackSubject, Observable
import numpy as np
from scipy.linalg import svd
import math


def solve_svd(A, b):
    # pinv
    x = np.linalg.pinv(A).dot(b)
    return x


def aperiodic_filter(signal, timeconst, delta, init=0):
    state = FeedbackSubject(init)
    error = signal - state
    newstate = (state + error * delta / timeconst)
    return state.loop(newstate)


def rxintegral(signal, delta, init=0):
    state = FeedbackSubject(init)
    newstate = (state + signal * delta)
    return state.loop(newstate)


def svd_backpack(target, signals, f=1):
    # Коэффициент f штрафут решение за чрезмерную длину полученного вектора
    nt = np.array([*target] + [0])
    ns = [np.array([*s] + [f], dtype=np.float64) for s in signals]

    for s in ns:
        s.shape = (s.shape[0], 1)

    matrix = np.hstack(ns)

    x = solve_svd(matrix, nt.T)
    return x


def rx_svd_backpack(target, signals, f=1):
    z = target.zip(*signals)
    return z.map(lambda x: svd_backpack(x[0], x[1:], f=f))
