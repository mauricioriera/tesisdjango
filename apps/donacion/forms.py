from django import forms
from apps.donacion.models import Donacion

class DateImput(forms.DateInput):
    '''
    Crea la estructura que tendra el campo date (fecha_donacion)
    '''
    imput_formats='%Y-%m-%d'
    input_type = 'date'

class DonacionForm(forms.ModelForm):
    '''
    Crea la estructura para los campos del modelo dado,labels(etiquetas) como se van a mostrar en el formulario
    y sus widgets correspondientes.
    '''
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