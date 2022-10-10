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

    def zip(*args):
        return Observable(reactivex.zip(*[a.collection_zipped_with(a) for a in args]))

    def subscribe(self, *args, **kwargs):
        return self.collection().subscribe(*args, **kwargs)

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
        return self.map(lambda x: p(arg, x))

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

    def to_list(self, count=None):
        if count is None:
            return self.collection().pipe(ops.to_list()).run()
        else:
            return self.o.range(0, count).to_list()

    def buffer_with_count(self, count):
        return Observable(self.collection().pipe(ops.buffer_with_count(count)))

    def sample(self, interval):
        return Observable(self.collection().pipe(ops.sample(interval)))


class Subject(Observable):
    def __init__(self, subject=None):
        if subject is None:
            subject = reactivex.subject.Subject()
        super().__init__(subject)

    def on_next(self, val):
        self.o.on_next(val)

    def on_completed(self):
        self.o.on_completed()


class Commutator(Subject):
    def __init__(self, observer=None):
        super().__init__()
        if observer is None:
            self.subscription = None
        else:
            self.bind(observer)

    def bind(self, observer):
        self.subscription = observer.subscribe(lambda x: self.on_next(x))

    def unbind(self):
        self.subscription.dispose()

    def rebind(self, observer):
        self.unbind()
        self.bind(observer)


class FeedbackSubject(Subject):
    def __init__(self, init=0, use_thread=False, subject=None):
        self.init = init
        if subject is None:
            subject = reactivex.subject.ReplaySubject()
        super().__init__(subject=subject)
        self.use_thread = use_thread

        if self.use_thread:
            self.cancel = False
            self.q = queue.Queue()
            self.thr = threading.Thread(target=self.foo)
            self.thr.start()

    def foo(self):
        while True:
            val = self.q.get()
            if self.cancel:
                return
            super().on_next(val)

    def on_next(self, val):
        if self.use_thread:
            self.q.put(val)
        else:
            super().on_next(val)

    def loop(self, newstate):
        self.subscription = newstate.subscribe(lambda x: self.on_next(x))
        self.on_next(self.init)
        return self

    def on_completed(self):
        self.subscription.dispose()
        if self.use_thread:
            self.cancel = True
            self.q.put(None)
            self.thr.join()
        return super().on_completed()


def rxinterval(d):
    return Observable(reactivex.interval(d))


def rxconstant(x, trigger=None):
    if trigger is None:
        class RxConstantObservable(Observable):
            def __init__(self, x):
                self.x = x
                self.collections = []

            def collection_zipped_with(self, oth):
                collection = reactivex.operators.map(lambda _: self.x)(
                    oth.collection())
                self.collections.append(collection)
                return collection

            def subscribe(self, *args, **kwargs):
                collection = reactivex.repeat_value(self.x)
                self.collections.append(collection)
                collection.subscribe(*args, **kwargs)

        return RxConstantObservable(x)
    else:
        return trigger.map(lambda _: x)


def rxrange(s, f):
    return Observable(reactivex.range(s, f))


def zip(*x):
    collections = []

    # first observable
    first_obsevable = None
    for a in x:
        if isinstance(a, Observable):
            first_obsevable = a
            break

    for a in x:
        if isinstance(a, Observable):
            collections.append(a.collection())
        else:
            constant = rxconstant(a)
            collections.append(constant.collection_zipped_with(first_obsevable))

    return Observable(reactivex.zip(*collections))


def from_iterable(x):
    return Observable(reactivex.from_iterable(x))
