from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend


class PieChart(Drawing):
    def __init__(self, width = 200, height= 200,*args,**kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self.add(Pie(), name='pie')
        self.add(Legend(), name='legend')


        self.pie.x = 110
        self.pie.y = -50
        self.pie.width = self.width - 20
        self.pie.height = self.height - 40
        self.pie.slices.label_pointer_piePad = 20  # Distance between the wafer and the label
        self.pie.slices.label_pointer_edgePad = 20  # The distance between the label and the outer
        self.pie.simpleLabels = 0  # 0 label on the right side of the label line; 1 on the line
        self.pie.sameRadii = 1  # 0 Pie chart is an ellipse; 1 Pie chart is a circle
        self.pie.pointerLabelMode = 'LeftRight'
        self.legend.x =300
        self.legend.y = -100
        self.legend.alignment = 'right'
        self.legend.fontSize = 15


    def data(self, data):
        self.pie.data = data

    def labels(self, labels):
        self.pie.labels = labels

    def legendcolorname(self,colorname):
        self.legend.colorNamePairs = colorname

    def slicefillcolor(self,colors):
        for i in range(len(colors)):
            self.pie.slices[i].fillColor=colors[i]