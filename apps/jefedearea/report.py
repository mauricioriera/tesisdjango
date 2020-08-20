from io import BytesIO
from django.views.generic.base import View
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from reportlab.platypus import Spacer,Table
from apps.jefedearea.piechart import PieChart
from apps.jefedearea.barchart import BarChart
from datetime import datetime as date
from apps.donador.models import Donador
from apps.donacion.models import Donacion
from reportlab.lib import colors
from operator import itemgetter


class Reporte(View):

    def get(self, request, *args, **kwargs):
        parm=self.kwargs.get('parm',0)
        response = HttpResponse(content_type='application/pdf')
        archivo = (date.now().strftime('reporte %d-%m-%y %H.%M.%S.pdf'))
        response['Content-Disposition'] = 'attachment; filename=%s' % archivo
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=A4,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=100,
                                bottomMargin=18,
                                )
        contenido = []
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.alignment = 1
        if(parm==1):
            title = Paragraph("Cantidad de Donantes Activos", title_style)
            contenido.append(title)
            contenido.append(self.__donantesactivos())
        if(parm==2):
            title = Paragraph("Cantidad de Donantes por Sexo", title_style)
            contenido.append(title)
            contenido.append(self.__donantessexo())
        if(parm==3):
            title = Paragraph("Cantidad de Donantes según Grupo/Factor", title_style)
            contenido.append(title)
            contenido.append(self.__donantesgrupofactor())
        if(parm==4):
            title = Paragraph("Cantidad de Donantes según Edad/Sexo", title_style)
            contenido.append(title)
            contenido.append(self.__donantesedadsexo())
        if(parm==5):
            title = Paragraph("Registro de Donaciones", title_style)
            contenido.append(title)
            contenido.append(self.tabla())
        doc.build(contenido)
        response.write(buff.getvalue())
        buff.close()
        return response
    def tabla(self):
        donaciones= Donacion.objects.prefetch_related('donador', 'user', 'hospital').values_list('donador__user__last_name',
                                                                                            'donador__user__first_name',
                                                                                            'fecha_donacion',
                                                                                            'donador__grupo_sanguineo',
                                                                                            'donador__factor_RH',
                                                                                            'hospital__nombre').order_by('-fecha_donacion')

        datos = (
                    ('Apellido', 'Nombre', 'Fecha Donacion', 'Grupo Sanguíneo', 'Factor RH',
                     'Centro Asistencial receptor'),) + tuple(donaciones)


        tabla = Table(data=datos,
                      style=[
                          ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                          ('BOX', (0, 0), (-1, -1), 2, colors.black),
                          ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                      ]
                      )
        return tabla

    def __donantesactivos(self):
        p = PieChart(300, 300)
        cantidad_total = Donador.objects.all().count()
        activos = [Donador.objects.filter(activo=True).count(), Donador.objects.filter(activo=False).count()]
        porcentajes = [str(round((activos[0] * 100 / cantidad_total), 2)),
                       str(round((activos[1] * 100 / cantidad_total), 2))]
        p.data(activos)
        p.legendcolorname([(colors.green, (f"{porcentajes[0]}% activos = {activos[0]} donantes")),
                           (colors.red, (f"{porcentajes[1]}% inactivos = {activos[1]} donantes"))])
        p.slicefillcolor([colors.green, colors.red])
        return p

    def __donantessexo(self):
        p = PieChart(300, 300)
        cantidad_total = Donador.objects.all().count()
        sexo = [Donador.objects.filter(genero='M').count(), Donador.objects.filter(genero='F').count()]
        porcentajes = [str(round((sexo[0] * 100 / cantidad_total), 2))
                    ,str(round((sexo[1] * 100 / cantidad_total), 2))]
        p.data(sexo)
        p.legendcolorname([(colors.yellow, (f"{porcentajes[0]}% masculino = {sexo[0]} donantes")),
                        (colors.red, (f"{porcentajes[1]}% femenino = {sexo[1]} donantes"))])
        p.slicefillcolor([colors.yellow,colors.red])
        return p
    def __donantesgrupofactor(self):
        b= BarChart()
        grupo = [(Donador.objects.filter(grupo_sanguineo='A', factor_RH='+').count(),
                  Donador.objects.filter(grupo_sanguineo='A', factor_RH='-').count(),
                  Donador.objects.filter(grupo_sanguineo='B', factor_RH='+').count(),
                  Donador.objects.filter(grupo_sanguineo='B', factor_RH='-').count(),
                  Donador.objects.filter(grupo_sanguineo='0', factor_RH='+').count(),
                  Donador.objects.filter(grupo_sanguineo='0', factor_RH='-').count(),
                  Donador.objects.filter(grupo_sanguineo='AB', factor_RH='+').count(),
                  Donador.objects.filter(grupo_sanguineo='AB', factor_RH='-').count())]
        b.data(grupo)
        b.colors([colors.blue])
        b.labels(['A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-'])
        b.yaxisname('Cantidad de Donantes')
        b.xaxisname('Grupo/Factor')
        return b
    def __donantesedadsexo(self):
        b=BarChart()
        edadh = [(d.calcularEdad) for d in Donador.objects.filter(genero='M')]
        edadm = [(d.calcularEdad) for d in Donador.objects.filter(genero='F')]
        l1,l2,l3,l4,l5,l6,l7,l8=([] for i in range(8))
        for i in edadh:
            if i >= 18 and i <= 30:
                l1.append(i)
            elif i > 30 and i < +40:
                l2.append(i)
            elif i > 40 and i <= 50:
                l3.append(i)
            else:
                l4.append(i)
        for i in edadm:
            if i >= 18 and i <= 30:
                l5.append(i)
            elif i > 30 and i < +40:
                l6.append(i)
            elif i > 40 and i <= 50:
                l7.append(i)
            else:
                l8.append(i)

        edadesh = [len(l1), len(l2), len(l3), len(l4)]
        edadesm = [len(l5), len(l6), len(l7), len(l8)]
        b.data([edadesh,edadesm])
        print (b.data)
        b.labels([('18-30'),('31-40'),('41-50'),('51-65')])
        b.colors([colors.blue, colors.red])
        b.yaxisname('Cantidad de Donantes')
        b.xaxisname('Rango de Edad')
        b.legendcolorname([(colors.blue,'Masculino'),(colors.red,'Femenino')])
        return b