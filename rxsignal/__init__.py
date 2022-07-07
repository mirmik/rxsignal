from rxsignal.observable import *
from rxsignal.filter import *
from rxsignal.dynsystem import *

def rxprint(x):
	x.subscribe(lambda x: print(x))