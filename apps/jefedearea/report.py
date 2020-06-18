from io import BytesIO
from typing import Tuple

from django.views.generic.base import View
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from apps.jefedearea.piechart import PieChart
from apps.jefedearea.barchart import BarChart
from datetime import datetime as date
from apps.donador.models import Donador
from reportlab.lib.colors import green, red, yellow,blue


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
            title = Paragraph("Cantidad de donantes Activos", title_style)
            contenido.append(title)
            contenido.append(self.__donantesactivos())
        if(parm==2):
            title = Paragraph("Cantidad de donantes por Sexo", title_style)
            contenido.append(title)
            contenido.append(self.__donantessexo())
        if(parm==3):
            title = Paragraph("Cantidad de donantes segun Grupo/Factor", title_style)
            contenido.append(title)
            contenido.append(self.__donantesgrupofactor())
        if(parm==4):
            title = Paragraph("Cantidad de donantes segun Edad/Sexo", title_style)
            contenido.append(title)
            contenido.append(self.__donantesedadsexo())
        doc.build(contenido)
        response.write(buff.getvalue())
        buff.close()
        return response

    def __donantesactivos(self):
        p = PieChart(300, 300)
        cantidad_total = Donador.objects.all().count()
        activos = [Donador.objects.filter(activo=True).count(), Donador.objects.filter(activo=False).count()]
        porcentajes = [str(round((activos[0] * 100 / cantidad_total), 2)),
                       str(round((activos[1] * 100 / cantidad_total), 2))]
        p.data(activos)
        p.legendcolorname([(green, (f"{porcentajes[0]}% activos = {activos[0]} donantes")),
                           (red, (f"{porcentajes[1]}% inactivos = {activos[1]} donantes"))])
        p.slicefillcolor([green, red])
        return p

    def __donantessexo(self):
        p = PieChart(300, 300)
        cantidad_total = Donador.objects.all().count()
        sexo = [Donador.objects.filter(genero='M').count(), Donador.objects.filter(genero='F').count()]
        porcentajes = [str(round((sexo[0] * 100 / cantidad_total), 2))
                    ,str(round((sexo[1] * 100 / cantidad_total), 2))]
        p.data(sexo)
        p.legendcolorname([(yellow, (f"{porcentajes[0]}% hombres = {sexo[0]} donantes")),
                        (red, (f"{porcentajes[1]}% mujeres = {sexo[1]} donantes"))])
        p.slicefillcolor([yellow,red])
        return p
    def __donantesgrupofactor(self):
        b= BarChart()
        grupo = [(Donador.objects.filter(grupo_sanguineo='A', factor_sanguineo='+').count(),
                  Donador.objects.filter(grupo_sanguineo='A', factor_sanguineo='-').count(),
                  Donador.objects.filter(grupo_sanguineo='B', factor_sanguineo='+').count(),
                  Donador.objects.filter(grupo_sanguineo='B', factor_sanguineo='-').count(),
                  Donador.objects.filter(grupo_sanguineo='0', factor_sanguineo='+').count(),
                  Donador.objects.filter(grupo_sanguineo='0', factor_sanguineo='-').count(),
                  Donador.objects.filter(grupo_sanguineo='AB', factor_sanguineo='+').count(),
                  Donador.objects.filter(grupo_sanguineo='AB', factor_sanguineo='-').count())]
        b.data(grupo)
        b.colors([blue])
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
        b.colors([blue, red])
        b.yaxisname('Cantidad de Donantes')
        b.xaxisname('Rango de Edad')
        b.legendcolorname([(blue,'Hombres'),(red,'Mujeres')])
        return b




'''def reporte(request):

     edadh=[(d.calcularEdad) for d in Donador.objects.filter(genero='M')]
    edadm=[(d.calcularEdad) for d in Donador.objects.filter(genero='F')]

    for i in edadh:
        if i>=18 and i<=30:
            lista1.append(i)
        elif i>30 and i<+40:
            lista2.append(i)
        elif i>40 and i<=50:
            lista3.append(i)
        else:
            lista4.append(i)
    for i in edadm:
        if i>=18 and i<=30:
            lista5.append(i)
        elif i>30 and i<+40:
            lista6.append(i)
        elif i>40 and i<=50:
            lista7.append(i)
        else:
            lista8.append(i)
    edadesh=[len(lista1),len(lista2),len(lista3),len(lista4)]
    edadesm=[len(lista5),len(lista6),len(lista7),len(lista8)]
    labels=[('18-30'),('31-40'),('41-50'),('51-65')]
    ind=np.arange(4)
    width=0.35
    p1 = plt.bar(ind, edadesh, width, color="blue")
    p2 = plt.bar(ind, edadesm, width,color="red",bottom=edadesh)
    plt.ylabel('cantidad de personas')
    plt.xticks(ind,labels)
    plt.yticks(np.arange(0, 10, 1))
    plt.legend((p1[0], p2[0]), ('Hombres', 'Mujeres'))
    pdf.savefig()
    plt.close()
   
    return redirect('inicio')'''