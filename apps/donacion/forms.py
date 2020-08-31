from django import forms
from apps.donacion.models import Donacion

class DateImput(forms.DateInput):
    '''
    @:param :
    '''
    imput_formats='%Y-%m-%d'
    input_type = 'date'

class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion

        fields = [
            'donador',
            'hospital',
            'fecha_donacion',
        ]
        labels = {
            'donador': 'Donante:',
            'hospital': 'Entidad receptora:',
            'fecha_donacion': 'Fecha de Donacion',
        }
        widgets = {
            'donador': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_donacion': DateImput(attrs={'class': 'form-control'}),
        }