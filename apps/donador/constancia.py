from django.http import HttpResponse
from datetime import datetime as date
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.views.generic.base import View
from apps.donador.models import Donador
from apps.empleado.models import Empleado
from apps.jefedearea.models import JefedeArea


class Constancia(View):

    def get(self,request,pk):

        donador =Donador.objects.get(pk=pk)
        query = JefedeArea.objects.filter(user=self.request.user).distinct() or Empleado.objects.filter(
            user=self.request.user).distinct()
        for e in query:
            hospital = e.hospital
        response=HttpResponse(content_type='application/pdf')
        archivo=(date.now().strftime('constancia de  donacion %d-%m-%y %H.%M.%S.pdf'))
        response['Content-Disposition']= 'attachmnet ; filename=%s' % archivo
        buffer=BytesIO()
        c=canvas.Canvas(buffer,pagesize=A4)


        c.setLineWidth(.3)
        if hospital.id == 1:
            c.drawImage('static/logos/logohospitalespanol.jpg', 40, 710)
        elif hospital.id == 2:
            c.drawImage('static/logos/logoschestakow.jpg', 40, 710)
        elif hospital.id == 3:
            c.drawImage('static/logos/logopoliclinica.jpg', 40, 710)
        elif hospital.id == 4:
            c.drawImage('static/logos/logoclinicaciudad.jpg', 40, 650)
        c.setFont('Helvetica',15)
        c.drawString(365,750,f'{hospital.nombre}')
        c.setFont('Helvetica',12)
        c.drawString(365,730,f'{hospital.direccion} Tel:{hospital.telefono}')
        c.setFont('Helvetica',18)
        c.drawString(110,690,'CONSTANCIA DE DONACIÓN DE SANGRE')
        c.line(110,688,475,688)
        c.setFont('Helvetica',12)
        c.drawString(110,645,f'Se deja constancia que señor/a { donador.user.first_name},{donador.user.last_name}')
        c.drawString(110,625,f'con DNI: {donador.dni} concurrio a donar sangre el dia de la fecha.')
        c.drawString(110,580,date.now().strftime('San Rafael, Mendoza %d-%m-%Y'))

        c.save()
        pdf= buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response