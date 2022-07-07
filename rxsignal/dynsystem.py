import numpy
from rxsignal.observable import feedback_subject

def dynsystem(g, A, B, init=None):
	if init is None:
		init = numpy.zeros(len(B))

	x0 = feedback_subject()
	x1 = x0.map(lambda a: numpy.matmul(A, a)) + g.map(lambda g: B*g)
	x1.subscribe(lambda a: x0.on_next(a))	
	x0.on_next(init)
	return x1

def dynsystem2(g, A, B, C, D, init):
	x0 = feedback_subject()
	x1 = numpy.matmul(A, x0) + numpy.matmul(B, g)
	y1 = numpy.matmul(C, x0) + numpy.matmul(D, g)
	x1.subscribe(lambda a: x0.on_next(a))	
	x0.on_next(init)
	return y1
	