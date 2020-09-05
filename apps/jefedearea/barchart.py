from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label


class BarChart (Drawing):

    def __init__(self, width=400, height=200, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self.add(VerticalBarChart(), name='chart')
        self.add(Label(), name='ylabel')
        self.add(Label(), name='xlabel')



        self.chart.x = 110
        self.chart.y = -80
        self.chart.width = self.width - self.chart.x - 10
        self.chart.height = self.height - self.chart.y - 10
        self.chart.barSpacing = 1
        self.ylabel.fontName = 'Helvetica'
        self.ylabel.fontSize = 15
        self.ylabel.angle = 90
        self.ylabel.x = 80
        self.ylabel.y = (self.chart.y + self.chart.height * 0.5)
        self.xlabel.fontSize = 15
        self.xlabel.height = 0
        self.xlabel.maxWidth = 100
        self.xlabel.fontName = 'Helvetica'
        self.xlabel.x = (self.chart.x + self.chart.width * 1.2)
        self.xlabel.y = -80




    def data(self, data):
        '''
        :param data:datos para generar el grafico
        :return:
        '''
        self.chart.data = data

    def colors(self,color):
        '''
        :param color: colores a usar en el grafico
        :return:
        '''
        for i in range(len(color)):
            self.chart.bars[i].fillColor= color[i]

    def labels(self,labels):
        '''
        :param labels: nombre de los datos
        :return:
        '''
        self.chart.categoryAxis.categoryNames=labels

    def yaxisname(self,namey):
        '''
        :param namey:nombre eje y del grafico
        :return:
        '''
        self.ylabel._text=namey

    def xaxisname(self,namex):
        '''
        :param namex:nombre del eje x del grafico
        :return:
        '''
        self.xlabel._text=namex

    def legendcolorname(self, colorname):
        '''
        :param colorname:colores que aprecera en las leyendas
        :return:
        '''
        self.add(Legend(), name='legend')
        self.legend.x = (self.chart.x + self.chart.width * 1.2)
        self.legend.y = 50
        self.legend.deltay = 8
        self.legend.fontName = 'Helvetica'
        self.legend.fontSize = 13
        self.legend.strokeWidth = 0.5
        self.legend.autoXPadding = 0
        self.legend.dy = 5
        self.legend.colorNamePairs = colorname