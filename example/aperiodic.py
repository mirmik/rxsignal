#!/usr/bin/env python3
from rxsignal import *
import rxsignal.flowchart

delta = 0.01
t = rxrange(0, 500) * delta
g = rxconstant(1, trigger=t)
# alternate: g = t.map(lambda x: 1)

x = FeedbackSubject(0)
y = x + (g - x) * delta
x.bind(y)

rxsignal.flowchart.flowplot_application(t, x)
