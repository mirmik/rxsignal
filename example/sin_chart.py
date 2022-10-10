#!/usr/bin/env python3
import rxsignal
import rxsignal.flowchart
import math

t = rxsignal.rxinterval(0.01) * 0.01
s = t.map(lambda x: math.sin(x*2))
c = t.map(lambda x: math.cos(x*2))

rxsignal.flowchart.flowplot_application(t, s, c)
