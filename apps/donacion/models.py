from django.db import models
from apps.donador.models import Donador
from apps.hospital.models import Hospital

# Create your models here.
class Donacion(models.Model):
    '''
    Modelo que correpsode a la tabla Donacion con sus campos.
    '''
    donador = models.ForeignKey(Donador, null=False, blank=False, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, null=False, blank=False, on_delete=models.CASCADE)
    fecha_donacion = models.DateField()