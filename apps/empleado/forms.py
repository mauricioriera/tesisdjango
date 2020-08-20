from django import forms
from apps.empleado.models import Empleado
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class DateImput(forms.DateInput):
    imput_formats='%Y-%m-%d'
    input_type = 'date'

class EmpleadoForm(forms.ModelForm):

    class Meta:

        model = Empleado

        fields = [
            'hospital',
            'fecha_nacimiento',
            'direccion',
            'telefono',
            'numero_legajo',
        ]
        labels = {
            'hospital': 'Centro Asistencial',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'numero_legajo': 'Número de Legajo',
        }
        widgets = {

            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': DateImput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_legajo': forms.TextInput(attrs={'class': 'form-control'}),
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