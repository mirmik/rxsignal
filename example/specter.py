#!/usr/bin/env python3
from reactivex import interval
from scipy.fft import rfftfreq
from rxsignal import *
import rxsignal.chart
import rxsignal.flowchart
import math
import random
import numpy

delta = 0.001

t = rxinterval(delta) * delta
s = t.map(lambda x: math.sin(x*(200))*random.random()
          + math.sin(x*1000)*random.random())

wind = s.buffer_with_count(256)

specter = (wind.map(numpy.fft.rfft)
           .map(lambda x: x.real**2 + x.imag**2))

freqs = wind.map(lambda x: numpy.fft.rfftfreq(len(x), d=delta))

rxsignal.chart.windowplot_application(freqs, specter)
