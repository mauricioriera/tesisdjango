from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index_hospital(request):
    return HttpResponse("soy la pagina hospital index")


# Create your views here.
