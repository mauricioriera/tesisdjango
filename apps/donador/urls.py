from django.urls import path
from apps.donador.views import index_donador

urlpatterns = [
    path('',index_donador),
]
