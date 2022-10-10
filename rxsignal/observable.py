import re
import reactivex
import reactivex.operators
import reactivex.operators as ops
import queue
import threading
import operator
import numpy
import math


class Observable:
    def __init__(self, o):
        self.o = o

    def collection(self):
        return self.o

    def map(self, foo):
        return Observable(self.collection().pipe(reactivex.operators.map(foo)))

    def collection_zipped_with(self, oth):
        """Hook for infinite generators such as rxconstant"""
        return self.collection()

    def zip(self, oth):
        return Observable(reactivex.zip(
            self.collection_zipped_with(oth),
            oth.collection_zipped_with(self)))

    def subscribe(self, *args, **kwargs):
        self.collection().subscribe(*args, **kwargs)

    def take(self, count):
        return Observable(self.collection().pipe(ops.take(count)))

    def op(self, p, arg):
        if isinstance(arg, Observable):
            z = self.zip(arg)
            return z.map(lambda x: p(x[0], x[1]))
        return self.map(lambda x: p(x, arg))

    def rop(self, p, arg):
        if isinstance(arg, Observable):
            z = self.zip(arg)
            return z.map(lambda x: p(x[1], x[0]))
        return self.map(lambda x: p(x, arg))

    def add(self, arg):
        return self.op(operator.add, arg)

    def sub(self, arg):
        return self.op(operator.sub, arg)

    def mul(self, arg):
        return self.op(operator.mul, arg)

    def div(self, arg):
        return self.op(operator.truediv, arg)

    def norm(self):
        return self.map(lambda x: numpy.linalg.norm(x))

    def radd(self, arg):
        return self.rop(operator.add, arg)

    def rsub(self, arg):
        return self.rop(operator.sub, arg)

    def rmul(self, arg):
        return self.rop(operator.mul, arg)

    def rdiv(self, arg):
        return self.rop(operator.truediv, arg)

    def sin(self):
        return self.map(lambda x: math.sin(x))

    def cos(self):
        return self.map(lambda x: math.cos(x))

    def __add__(self, oth):
        return self.add(oth)

    def __sub__(self, oth):
        return self.sub(oth)

    def __mul__(self, oth):
        return self.mul(oth)

    def __truediv__(self, oth):
        return self.div(oth)

    def __radd__(self, oth):
        return self.radd(oth)

    def __rsub__(self, oth):
        return self.rsub(oth)

    def __rmul__(self, oth):
        return self.rmul(oth)

    def __rtruediv__(self, oth):
        return self.rdiv(oth)

    def __neg__(self):
        return self.map(lambda x: -x)

    def __getitem__(self, idx):
        return self.map(lambda x: x[idx])

    def to_list(self, count):
        return self.o.range(0, count).to_list()


class Subject(Observable):
    def __init__(self, subject=None):
        if subject is None:
            subject = reactivex.subject.Subject()
        super().__init__(subject)

    def on_next(self, val):
        self.o.on_next(val)


class FeedbackSubject(Subject):
    def __init__(self, init=0):
        self.init = init
        super().__init__(subject=reactivex.subject.ReplaySubject())
        self.q = queue.Queue()
        self.thr = threading.Thread(target=self.foo)
        self.thr.start()

    def foo(self):
        while True:
            val = self.q.get()
            super().on_next(val)

    def on_next(self, val):
        self.q.put(val)

    def loop(self, newstate):
        newstate.subscribe(lambda x: self.on_next(x))
        self.on_next(self.init)
        return self


def rxinterval(d):
    return Observable(reactivex.interval(d))


def rxconstant(x):
    class RxConstantObservable(Observable):
        def __init__(self, x):
            self.x = x
            self.collections = []

        def collection_zipped_with(self, oth):
            print("collection_zipped_with", self, oth)
            collection = reactivex.operators.map(lambda _: self.x)(
                oth.collection())
            self.collections.append(collection)
            return collection

        def subscribe(self, *args, **kwargs):
            collection = reactivex.repeat_value(self.x)
            self.collections.append(collection)
            collection.subscribe(*args, **kwargs)

    return RxConstantObservable(x)


def rxrange(s, f):
    return Observable(reactivex.range(s, f))


def zip(*x):
    return Observable(reactivex.zip(*[a.o for a in x]))
