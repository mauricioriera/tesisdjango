from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index_donador(request):
    return HttpResponse("Soy pagina donador index")

# Create your views here.
