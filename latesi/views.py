from django.shortcuts import render


def inicio(request):
    context = {'foo': 'bar'}
    return render(request, 'index.html', context)