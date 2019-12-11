from django import forms
from apps.donador.models import Donador
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DonadorForm(forms.ModelForm):
    class Meta:
        model = Donador

        fields = [
            'hospital',
            'fecha_nacimiento',
            'direccion',
            'telefono',
            'genero',
            'grupo_sanguineo',
            'factor_sanguineo',
        ]
        labels = {
            'hospital': 'Hospital:',
            'fecha_nacimiento': 'Fecha de Nacimiento:',
            'direccion': 'Direccion:',
            'telefono': 'Telefono:',
            'genero': 'Genero:',
            'grupo_sanguineo': 'Grupo Sanguineo:',
            'factor_sanguineo': 'Factor Sanguineo:',
        }
        widgets = {
            'hospital': forms.Select,
            'fecha_nacimiento': forms.SelectDateWidget(years=range(1950, 2100)),
            'direccion': forms.TextInput,
            'telefono': forms.TextInput,
            'genero': forms.Select,
            'grupo_sanguineo': forms.Select,
            'factor_sanguineo': forms.Select,
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
            'username': 'Usuario:',
            'first_name': 'Nombre:',
            'last_name': 'Apellido:',
            'email': 'Correo:',
        }