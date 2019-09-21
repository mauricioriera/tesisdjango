from django.db import models

from apps.hospital.models import Hospital
# Create your models here.
class Donador(models.Model):
    hospital =models.ForeignKey(Hospital, null=True, blank=True, on_delete= models.SET_NULL)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido = models.CharField(max_length=50, null=False, blank=False)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=50,null=False,blank=False)
    sexo = models.CharField(max_length=10,null=False,blank=False)
    grupo_sanguineo = models.CharField(max_length=10,null=False,blank=False)
    factor_sanguineo = models.CharField(max_length=10,null=False,blank=False)
    email = models.EmailField()
    telefono = models.CharField(max_length=12)
    activo = models.BooleanField()




