from django import forms
from apps.donador.models import Donador
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class DateImput(forms.DateInput):
    imput_formats='%Y-%m-%d'
    input_type = 'date'

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
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': DateImput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'grupo_sanguineo': forms.Select(attrs={'class': 'form-control'}),
            'factor_sanguineo': forms.Select(attrs={'class': 'form-control'}),
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
class ModificarForm(UserChangeForm):
    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        labels = {
            'username': 'Usuario:',
            'first_name': 'Nombre:',
            'last_name': 'Apellido:',
            'email': 'Correo:',
            'password':'Contaseña',
        }