from django import forms
from apps.empleado.models import Empleado
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EmpleadoForm(forms.ModelForm):

    class Meta:

        model = Empleado

        fields = [
            'hospital',
            'fecha_nacimiento',
            'direccion',
            'telefono',
            'numero_legajo',
            'groups',
        ]
        labels = {
            'hospital': 'Hospital',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Direccion',
            'telefono': 'Telefono',
            'numero_legajo': 'Numero de Legajo',
            'groups': 'grupo',
        }
        widgets = {

            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_legajo': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.Select(attrs={'class': 'form-control'}),
        }

class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'Nombre de usuario',
            'first_name':'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo',
        }