from django import forms
from apps.jefedearea.models import JefedeArea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class JefedeAreaForm(forms.ModelForm):

    class Meta:

        model = JefedeArea

        fields = [
            'hospital',
            'fecha_nacimiento',
            'direccion',
            'telefono',
            'numero_legajo',
        ]
        labels = {
            'hospital': 'Hospital',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Direccion',
            'telefono': 'Telefono',
            'numero_legajo': 'Numero de Legajo',
        }
        widgets = {

            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.SelectDateWidget(attrs={'class': 'form-control'}),
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