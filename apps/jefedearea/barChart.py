from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.legends import Legend,colors
from reportlab.graphics.charts.piecharts import Pie
from apps.donador.models import Donador




class BarChart(Drawing):
    def __init__(self, width=400, height=200, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self.add(String(200, 180, 'Hello World'), name='title')
        self.add(Pie(), name='pie')
        self.add(Legend(), name='leyenda')
        h=Donador.objects.filter(genero='M').count()
        m=Donador.objects.filter(genero='F').count()
        datos = [(colors.yellow, 'Hombres'), (colors.red, 'Mujeres')]

        self.title.fontName = 'Helvetica-Bold'
        self.title.fontSize = 12
        self.pie.slices[0].fillColor=colors.yellow
        self.pie.slices[1].fillColor=colors.red
        self.pie([h, m],autopct="%1.1f%%")
        self.pie.data = [h, m]
        self.pie.x = 50
        self.pie.y = 0
        self.pie.width = 150
        self.pie.height = 150
        self.leyenda.x= 300
        self.leyenda.y=100
        self.leyenda.colorNamePairs = datos





if __name__ == '__main__':
    BarChart().save(formats=['gif', 'png', 'jpg', 'pdf'], outDir='.', fnRoot='barchart')