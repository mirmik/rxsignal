import reactivex
import queue
import threading
import operator

class observable:
    def __init__(self, o):
        self.o = o

    def map(self, foo):
        return observable(self.o.pipe(reactivex.operators.map(foo)))

    def zip(self, oth):
        return observable(reactivex.zip(self.o, oth.o))        

    def subscribe(self, *args, **kwargs):
        self.o.subscribe(*args, **kwargs)

    def take(self, count):
        return observable(self.o.pipe(ops.take(count)))

    def op(self, p, arg):
        if isinstance(arg, observable):
            z = self.zip(arg)
            return z.map(lambda x: p(x[0], x[1]))

        return self.map(lambda x: p(x, arg))

    def add(self, arg):
        return self.op(operator.add, arg)
    def sub(self, arg):
        return self.op(operator.sub, arg)
    def mul(self, arg):
        return self.op(operator.mul, arg)
    def div(self, arg):
        return self.op(operator.truediv, arg)
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

class subject(observable):
    def __init__(self, subject=None):
        if subject is None:
            subject = reactivex.subject.Subject()
        super().__init__(subject)

    def on_next(self, val):
        self.o.on_next(val)

class feedback_subject(subject):
    def __init__(self):
        super().__init__(subject = reactivex.subject.ReplaySubject())
        self.q = queue.Queue()
        self.thr = threading.Thread(target=self.foo)
        self.thr.start()

    def foo(self):
        while True:
            val = self.q.get()
            super().on_next(val)

    def on_next(self, val):
        self.q.put(val)


def rxinterval(d):
    return observable(reactivex.interval(d))

def rxrange(s,f):
    return observable(reactivex.range(s,f))