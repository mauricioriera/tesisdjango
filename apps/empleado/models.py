from django.db import models
from django.contrib.auth.models import User

from apps.hospital.models import Hospital


# Create your models here.
class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=50,null=False,blank=False)
    telefono = models.CharField(max_length=12)
    numero_legajo = models.IntegerField()

