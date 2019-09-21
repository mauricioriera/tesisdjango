
from django.urls import path
from apps.empleado.views import EmpleadoCrear,EmpleadoLista,EmpleadoModificar,EmpleadoBorrar,validacion

urlpatterns = [

    path('validar/',validacion,name='validar_usuario'),
    path('nuevo/',EmpleadoCrear.as_view(), name= 'empleado_crear'),
    path('listar/',EmpleadoLista.as_view(),name= 'empleado_listar'),
    path('modificar/<int:pk>/',EmpleadoModificar.as_view(),name='empleado_modificar'),
    path('borrar/<int:pk>/',EmpleadoBorrar.as_view(),name='empleado_borrar')
    
]
