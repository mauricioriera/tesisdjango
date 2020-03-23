from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.jefedearea.views import JefedeAreaCrear,JefedeAreaLista,JefedeAreaModificar,JefedeAreaBorrar,perfil,preperfil

urlpatterns =[
    path('nuevo/',login_required(JefedeAreaCrear.as_view()), name= 'jefedearea_crear'),
    path('listar/',login_required(JefedeAreaLista.as_view()), name= 'jefedearea_listar'),
    path('preperfil/',login_required(preperfil.as_view()),name='preperfil_jefedearea'),
    path('perfil/<int:pk>/',login_required(perfil),name='perfil_jefedearea'),
    path('modificar/<int:pk>/',login_required(JefedeAreaModificar.as_view()),name='jefedearea_modificar'),
    path('borrar/<int:pk>/',login_required(JefedeAreaBorrar.as_view()),name='jefedearea_borrar'),
]