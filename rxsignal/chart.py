
from PyQt5.QtChart import (
    QChart, QChartView, QValueAxis, QCategoryAxis,
    QLineSeries, QSplineSeries)

from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import QPoint, QPointF
import PyQt5.QtCore

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from numpy import array
import reactivex
import rxsignal


class WindowChart(QChart):
    def __init__(self):
        super().__init__()

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

        self.setAxisX(self.axisX)
        self.setAxisY(self.axisY)

        self.ymin = float('inf')
        self.ymax = float('-inf')
        self.xmin = float('inf')
        self.xmax = float('-inf')

    def add_xyseries(self, type=QLineSeries):
        series = type()
        series.setUseOpenGL(True)
        self.addSeries(series)
        series.attachAxis(self.axisX)
        series.attachAxis(self.axisY)
        return series

    def set_yrange(self, ymin, ymax):
        self.axisY.setRange(ymin, ymax)

    def set_xrange(self, xmin, xmax):
        self.axisX.setRange(xmin, xmax)


def create_windowchart(xobservable, yobservable, live_autoscale=False):
    chart = WindowChart()
    series = chart.add_xyseries()
    view = QChartView(chart)

    def update(tpl):
        # series.clear()
        array = []

        if live_autoscale:
            chart.ymin = float('inf')
            chart.ymax = float('-inf')
            chart.xmin = float('inf')
            chart.xmax = float('-inf')

        for i in range(len(tpl[0])):
            x = tpl[0][i]
            y = tpl[1][i]
            array.append(QPointF(x, y))
            if y < chart.ymin:
                chart.ymin = y
            if y > chart.ymax:
                chart.ymax = y
            if x < chart.xmin:
                chart.xmin = x
            if x > chart.xmax:
                chart.xmax = x
        chart.set_xrange(chart.xmin, chart.xmax)
        chart.set_yrange(chart.ymin, chart.ymax)
        series.replace(array)
        # chart.update()

    xobservable.zip(yobservable).subscribe(update)
    return view


def windowplot_application(*args, **kwargs):
    app = QtWidgets.QApplication(sys.argv)
    view = create_windowchart(*args, **kwargs)
    view.resize(800, 600)
    view.show()
    return app.exec()
