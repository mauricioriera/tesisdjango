from django.db import models
from django.contrib.auth.models import User, Group

from apps.hospital.models import Hospital
from datetime import date

class JefedeArea(models.Model):
    '''
    Modelo que corresponde a la tabla JefedeArea con sus campos
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=50, null=False, blank=False)
    telefono = models.CharField(max_length=12)
    numero_legajo = models.IntegerField()

    @property
    def calcularEdad(self):
        '''
        calculo de edad
        :return: edad
        '''
        days_in_year = 365.2425
        age = int((date.today() - self.fecha_nacimiento).days / days_in_year)
        return age
