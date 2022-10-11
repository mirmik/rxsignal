#!/usr/bin/env python3
from rxsignal import *
import rxsignal.flowchart

delta = 0.1
t = rxrange(0, 200) * delta
g1 = rxconstant(1, trigger=t)
g2 = rxconstant(0, trigger=t)

x = FeedbackSubject(0)
y1 = x + (g1 - x) * delta
y2 = x + (g2 - x) * delta

cond = t.map(lambda t: t % 4 < 2)
y = rxchoose(cond, y1, y2)
x.bind(y)

rxsignal.flowchart.flowplot_application(t, x, cond)
