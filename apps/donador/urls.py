from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.donador.views import DonadorCrear, DonadorLista, activacion, DonadorModificar, DonadorEliminar,preperfil,perfil,hilo,Desactivar
from apps.donador.constancia import Constancia
urlpatterns = [
    path('crear/',DonadorCrear.as_view(), name='crear_donante'),
    path('preperfil/',login_required(preperfil.as_view()), name='preperfil_donante'),
    path('perfil/<int:pk>',login_required(perfil),name='perfil_donante'),
    path('listar_donantes/',login_required(DonadorLista.as_view()), name='lista_donante'),
    path('modificar_donante/<int:pk>/',login_required(DonadorModificar.as_view()), name='modificar_donante'),
    path('eliminar_donante/<int:pk>/',login_required(DonadorEliminar.as_view()), name='eliminar_donante'),
    path('activacion/<int:pk>/',login_required(activacion), name='activar_donante'),
    path('desactivacion/<int:pk>/',login_required(Desactivar.as_view()), name='desactivar_donante'),
    path('enviar_mail/<int:pk>/',login_required(hilo),name='enviarmail_donante'),
    path('constancia/<int:pk>/',login_required(Constancia.as_view()),name='constancia_donante'),
]
