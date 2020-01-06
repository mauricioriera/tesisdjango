
from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.empleado.views import EmpleadoCrear,EmpleadoLista,EmpleadoModificar,EmpleadoBorrar,perfil,preperfil

urlpatterns = [
    path('nuevo/',login_required(EmpleadoCrear.as_view()), name= 'empleado_crear'),
    path('listar/',login_required(EmpleadoLista.as_view()), name= 'empleado_listar'),
    path('preperfil/',login_required(preperfil.as_view()),name='preperfil_empleado'),
    path('perfil/<int:pk>/',login_required(perfil),name='perfil_empleado'),
    path('modificar/<int:pk>/',login_required(EmpleadoModificar.as_view()),name='empleado_modificar'),
    path('borrar/<int:pk>/',login_required(EmpleadoBorrar.as_view()),name='empleado_borrar')
]
