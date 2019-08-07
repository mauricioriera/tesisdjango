from django import forms
from apps.empleado.models import Empleado


class EmpleadoForm(forms.ModelForm):

    class Meta:

        model= Empleado

        fields = [
            'hospital',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'direccion',
            'email',
            'telefono',
            'numero_legajo',
        ]
        labels = {
            'hospital': 'Hospital',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Direccion',
            'email': 'E-mail',
            'telefono': 'Telefono',
            'numero_legajo': 'Numero de Legajo',
        }
        widgets = {
            'hospital': forms.Select(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellido': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nacimiento': forms.SelectDateWidget(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
            'numero_legajo':forms.TextInput(attrs={'class':'form-control'}),
        }
