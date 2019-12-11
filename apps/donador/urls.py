from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.donador.views import DonadorCrear, DonadorLista, activacion, DonadorModificar, DonadorEliminar

urlpatterns = [
    path('crear/',DonadorCrear.as_view(), name='crear_donante'),
    path('listar_donantes/',login_required(DonadorLista.as_view()), name='lista_donante'),
    path('modificar_donante/<int:pk>/',login_required(DonadorModificar.as_view()), name='modificar_donante'),
    path('eliminar_donante/<int:pk>/',login_required(DonadorEliminar.as_view()), name='eliminar_donante'),
    path('cambiar_activacion/<int:pk>/',login_required(activacion), name='activar_donante')
]
