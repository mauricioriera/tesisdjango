
from django.urls import path
from apps.hospital.views import index_hospital

urlpatterns = [
    path('',index_hospital),
]
