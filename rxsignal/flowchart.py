
from time import time
from PyQt5.QtChart import (
    QChart, QChartView, QValueAxis, QCategoryAxis,
    QLineSeries, QSplineSeries)

from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import QPoint, QPointF
import PyQt5.QtCore

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import reactivex
import rxsignal
import time


class FlowSeries:
    def __init__(self, maxinterval=None, maxpoints=None, type=QLineSeries):
        self.maxpoints = maxpoints
        self.maxinterval = maxinterval

        self.data = []
        self.ymin = 0
        self.ymax = 0

        self.series = type()
        self.series.setUseOpenGL(True)
        self.series.append(self.data)

        self.last_timestamp = 0

    def attachAxes(self, x, y):
        self.series.attachAxis(x)
        self.series.attachAxis(y)

    def append(self, point, timestamp):
        if len(self.data) != 0 and timestamp < self.last_timestamp:
            self.data.clear()

        self.data.append(point)

        if self.maxinterval is not None:
            while self.data[-1].x() - self.data[0].x() > self.maxinterval:
                del self.data[0]

        if self.maxpoints is not None:
            while len(self.data) > self.maxpoints:
                del self.data[0]

        if point.y() < self.ymin:
            self.ymin = point.y()
        if point.y() > self.ymax:
            self.ymax = point.y()

        self.last_timestamp = timestamp

    def append_xy(self, point):
        self.data.append(point)

        if point.y() < self.ymin:
            self.ymin = point.y()
        if point.y() > self.ymax:
            self.ymax = point.y()

        if self.maxinterval is not None:
            while self.data[-1].x() - self.data[0].x() > self.maxinterval:
                del self.data[0]

        if self.maxpoints is not None:
            while len(self.data) > self.maxpoints:
                del self.data[0]

    def xrange(self):
        if len(self.data) == 0:
            return 0, 0

        first_x = self.data[0].x()
        last_x = self.data[-1].x()
        return first_x, last_x

    def yrange(self):
        return self.ymin, self.ymax

    def replace(self):
        self.series.replace(self.data)


class FlowChart(QChart):
    def __init__(self, yautoscale=True):
        super().__init__()
        self.series_list = []
        self.last_timestamp = time.time()

        self.ymin = 0
        self.ymax = 0
        self.yautoscale = yautoscale

        self.axisX = QValueAxis()
        self.axisY = QValueAxis()

        self.axisPen = QPen(PyQt5.QtCore.Qt.red)
        self.axisPen.setWidth(4)
        self.axisX.setLinePen(self.axisPen)
        self.axisY.setLinePen(self.axisPen)

        self.axixBrush = QBrush(PyQt5.QtCore.Qt.green)
        self.axisX.setLabelsBrush(self.axixBrush)
        self.axisX.setGridLineVisible(True)
        self.axisY.setLabelsBrush(self.axixBrush)
        self.axisY.setGridLineVisible(True)

        self.axisY.setRange(0, 28)

        self.setAxisX(self.axisX)
        self.setAxisY(self.axisY)

    def add_xyseries(self, maxinterval, maxpoints=None, type=QLineSeries):
        series = FlowSeries(
            maxinterval=maxinterval, maxpoints=maxpoints, type=type)
        self.addSeries(series.series)
        series.attachAxes(self.axisX, self.axisY)
        self.series_list.append(series)
        return series

    def set_yrange(self, ymin, ymax):
        self.axisY.setRange(ymin, ymax)

    def update(self):
        xmin = None
        xmax = None
        ymin = None
        ymax = None

        for s in self.series_list:
            r = s.xrange()
            if xmin is None or xmin > r[0]:
                xmin = r[0]
            if xmax is None or xmax < r[1]:
                xmax = r[1]

        if self.yautoscale:
            for s in self.series_list:
                r = s.yrange()
                if ymin is None or ymin > r[0]:
                    ymin = r[0]
                if ymax is None or ymax < r[1]:
                    ymax = r[1]

        #timestamp = time.time()

        # if timestamp - self.last_timestamp > 0.1:
        for s in self.series_list:
            self.axisX.setRange(xmin, xmax)
            self.axisY.setRange(ymin, ymax)
            s.replace()
        #self.last_timestamp = timestamp


def create_flowchart(xobservable,
                     *yobservable,
                     interval=None,
                     maxpoints=None,
                     autoscale=True,
                     yrange=(-1, 1)):
    yobservable2 = []
    if isinstance(xobservable, rxsignal.Observable):
        xobservable = xobservable.o
    for i in range(len(yobservable)):
        # if isinstance(yobservable[i], rxsignal.Observable):
        yobservable2.append(yobservable[i].o)

    serieses = []
    l = len(yobservable)

    def update(x):
        try:
            for i in range(l):
                serieses[i].append_xy(QPointF(x[0], x[1+i]))
            chart.update()
        except Exception as e:
            print(e, x)
            pass

    chart = FlowChart(yautoscale=autoscale)
    for y in yobservable:
        serieses.append(chart.add_xyseries(maxinterval=interval,
                                           maxpoints=maxpoints))
    view = QChartView(chart)
    chart.set_yrange(*yrange)

    a = reactivex.zip(xobservable, *yobservable2)
    a.subscribe(update)

    return view


def flowplot_application(*args, **kwargs):
    app = QtWidgets.QApplication(sys.argv)
    view = create_flowchart(*args, **kwargs)
    view.resize(800, 600)
    view.show()
    return app.exec()
