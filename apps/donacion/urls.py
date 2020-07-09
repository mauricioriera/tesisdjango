from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.donacion.views import DonacionCrear

urlpatterns = [
    path('donacion/',login_required(DonacionCrear.as_view()),name='donacion')

]