from django.db import models
from django.contrib.auth.models import User,Group

from apps.hospital.models import Hospital
from datetime import date

# Create your models here.
class Donador(models.Model):

    GENERO = (
        ('M', 'masculino'),
        ('F', 'femenino'),
    )
    GRUPO_SANGRE = (
        ('A','A'),
        ('B','B'),
        ('AB','AB'),
        ('0','0'),
    )
    FACTOR_SANGRE=(
        ('+', 'positivo'),
        ('-', 'negativo'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=50,null=False,blank=False)
    genero = models.CharField( max_length=1 , choices = GENERO, default='M')
    grupo_sanguineo = models.CharField(max_length=10,choices=GRUPO_SANGRE, default='A')
    factor_sanguineo = models.CharField(max_length=2, choices=FACTOR_SANGRE, default='+')
    telefono = models.CharField(max_length=12)
    activo = models.BooleanField(default=0)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def calcularEdad(self):
        days_in_year =365.2425
        age = int((date.today() - self.fecha_nacimiento).days / days_in_year)
        return age