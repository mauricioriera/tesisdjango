from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout


def inicio(request):
    context = {'foo': 'bar'}
    return render(request, 'index.html', context)

def validacion(request):
        if request.user.groups.filter(name="Donantes").exists():
             return redirect('lista_donante')
        elif request.user.groups.filter(name="Empleado").exists():
            return redirect('empleado_listar')
        elif request.user.groups.filter(name="Jefe de Área").exists():
            return redirect('empleado_crear')

def logout(request):
    do_logout(request)
    return redirect('inicio')