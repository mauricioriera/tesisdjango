from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.empleado.forms import EmpleadoForm


def index(request):
    return render(request, 'empleado/index.html')


def empleado_view(request):
    if request.method == 'POST' :
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('empleado:empleado_index')
    else:
        form = EmpleadoForm()

    return render(request, 'empleado/empleado_formulario.html', {'form':form,})
