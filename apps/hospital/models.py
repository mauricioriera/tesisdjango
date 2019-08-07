from django.db import models

# Create your models here.
class Hospital(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    direccion = models.CharField(max_length=50,null=False,blank=False)
    email = models.EmailField()
    telefono = models.CharField(max_length=12)

    def __str__(self):
        return '{}'.format(self.nombre)
