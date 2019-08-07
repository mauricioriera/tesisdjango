from django.db import models

from apps.hospital.models import Hospital


# Create your models here.
class Empleado(models.Model):
    hospital =models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido = models.CharField(max_length=50, null=False, blank=False)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=50,null=False,blank=False)
    email = models.EmailField()
    telefono = models.CharField(max_length=12)
    numero_legajo = models.IntegerField()
