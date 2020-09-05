from django.db import models

# Create your models here.
class Hospital(models.Model):
    '''
    modelo que corresponde al tabla hospital con sus campos
    '''
    nombre = models.CharField(max_length=50, null=False, blank=False)
    direccion = models.CharField(max_length=50,null=False,blank=False)
    email = models.EmailField()
    telefono = models.CharField(max_length=12)
    logo=models.ImageField(upload_to='static/logos')

    def __str__(self):
        return '{}'.format(self.nombre)
