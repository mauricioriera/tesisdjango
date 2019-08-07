
from django.urls import path
from apps.empleado.views import index,empleado_view

urlpatterns = [
    path('index/',index, name= 'empleado_index'),
    path('nuevo/',empleado_view, name= 'empleado_crear'),
]
