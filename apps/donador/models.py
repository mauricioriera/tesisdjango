from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User,Group

from apps.hospital.models import Hospital
from datetime import date

def check_date(value):
    days_in_year = 365.2425
    age = int((date.today() -value).days / days_in_year)
    if age<18 or age>65:
        raise ValidationError('No se permiten registrar menores de 18 años ni mayores de 65 años ')
    return value

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
    fecha_nacimiento = models.DateField(validators=[check_date])
    direccion = models.CharField(max_length=50,null=False,blank=False)
    genero = models.CharField( max_length=1 , choices = GENERO, default='M')
    grupo_sanguineo = models.CharField(max_length=10,choices=GRUPO_SANGRE, default='A')
    factor_RH = models.CharField(max_length=2, choices=FACTOR_SANGRE, default='+')
    telefono = models.CharField(max_length=12)
    dni = models.IntegerField()
    activo = models.BooleanField(default=0)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def calcularEdad(self):
        days_in_year =365.2425
        age = int((date.today() - self.fecha_nacimiento).days / days_in_year)
        return age
    def __str__(self):
        return '{}'.format(self.user.username)

class Desactivar(models.Model):
    donador = models.ForeignKey(Donador,on_delete=models.CASCADE)
    motivo= models.IntegerField()
    fecha_desactivar=models.DateField()