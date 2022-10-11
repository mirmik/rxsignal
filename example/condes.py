#!/usr/bin/env python3
from rxsignal import *
import rxsignal.flowchart

delta = 0.1
t = rxrange(0, 200) * delta
g1 = rxconstant(0, trigger=t)
g2 = rxconstant(1, trigger=t)
g3 = rxconstant(2, trigger=t)
g4 = rxconstant(3, trigger=t)

x = FeedbackSubject(0)
y1 = x + (g1 - x) * delta
y2 = x + (g2 - x) * delta
y3 = x + (g3 - x) * delta
y4 = x + (g4 - x) * delta


def choose(t, *sigs):
    pass


y = t.zip(y1, y2, y3, y4).map(choose)

rxsignal.flowchart.flowplot_application(t, x)
