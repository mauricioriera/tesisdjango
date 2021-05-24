from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from apps.donacion.models import Donacion
from apps.donacion.forms import DonacionForm
from apps.donador.models import Donador,Desactivar
from apps.jefedearea.models import JefedeArea
from apps.empleado.models import Empleado
from django.contrib import messages



class DonacionCrear (AccessMixin,CreateView):
    '''
    premite crear un objeto del modelo Donacion y denegar o conceder al acceso segun el rol del usuario
    '''
    model = Donacion
    form_class = DonacionForm
    template_name = 'donacion/registrodonacion.html'
    success_url = reverse_lazy('lista_donante')

    def get(self, request, pk):
        '''
        :param request: para hacer solicitud HTTP(GET), para que traiga la pagina web solicitada
        :param pk: llave primaria del objeto Donacion
        :return: retorna un template que se usa para cargar la donacion
        '''
        d = Donador.objects.get(pk=pk)
        query = JefedeArea.objects.filter(user=self.request.user).distinct() or Empleado.objects.filter(
            user=self.request.user).distinct()
        for e in query:
            hospital= e.hospital
        return render(request, 'donacion/registrodonacion.html', {'donador': d,'hospital': hospital, 'form':self.form_class})

    def post(self, request, *args, **kwargs):
        '''
        :param request:para hacer solicitud HTTP(POST), para enviar datos.
        :return: si el onbjeto fue cargado correctamente nos envia a la pagina lista de donantes si no nos muestra el error
        para cargar de nuevo correctamente el objeto.
        '''

        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            donacion = form.save(commit=False)
            donacion.save()
            donador=donacion.donador
            donador.activo = False
            donador.save()
            desactivar=Desactivar()
            desactivar.donador=donador
            desactivar.motivo= 5
            desactivar.fecha_desactivar=donacion.fecha_donacion
            desactivar.save()
            messages.add_message(request, messages.SUCCESS, 'donacion registrada')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request, messages.ERROR, 'donacion no registrada')
            return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        '''
        :param request: solicitud HTTP(GET) que pregunta si el usuario esta autenticado y que rol tiene
        :return:template de error si es un rol de Donantes si no muestra la pagina de Donaciones
        '''
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name="Donantes").exists():
           return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)