from django import forms
from apps.donacion.models import Donacion

class DateImput(forms.DateInput):
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
            'donador': 'donante',
            'hospital': 'Hospital receptor',
            'fecha_donacion': 'Fechs de Donacion',
        }
        widgets = {
            'donador': forms.Select(attrs={'class': 'form-control'}),
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'fecha_donacion': DateImput(attrs={'class': 'form-control'}),
        }