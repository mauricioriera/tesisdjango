
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from apps.donador.forms import DonadorForm, RegistroForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from apps.donador.models import Donador
from django.contrib.auth.models import Group, User


def activacion(request,pk):
    donador = get_object_or_404(Donador, pk=pk)
    if donador.activo == False:
        donador.activo = True
        donador.save()
    else:
        donador.activo = False
        donador.save()
    return redirect('lista_donante')


class DonadorCrear(CreateView):
    model = Donador
    form_class = DonadorForm
    second_form_class = RegistroForm
    template_name = 'donador/registro.html'
    success_url = reverse_lazy('inicio')

    def get_context_data(self, **kwargs):
        context = super(DonadorCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] =self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            donador = form.save(commit=False)
            donador.user = form2.save()
            donador.save()
            g = Group.objects.get(name='Donantes')
            g.user_set.add(donador.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class DonadorLista(ListView):
    model = Donador
    template_name = 'donador/donador_lista.html'

class DonadorModificar(UpdateView):
    model = Donador
    second_model = User
    form_class = DonadorForm
    second_form_class = RegistroForm
    template_name = 'donador/registro.html'
    success_url = reverse_lazy('datos_donante')

    def get_context_data(self, **kwargs):
        context = super(DonadorModificar, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        donador = self.model.objects.get(id=pk)
        user = self.second_model.objects.get(id=donador.user_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=user)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_donador = kwargs['pk']
        donador = self.model.objects.get(id=id_donador)
        user = self.second_model.objects.get(id=donador.user_id)
        form2 = self.second_form_class(request.POST, instance=user)
        form = self.form_class(request.POST, instance=donador)
        if form.is_valid() and form2.is_valid():
            form2.save()
            form.save()
            g = Group.objects.get(name='Donantes')
            g.user_set.add(donador.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

class DonadorEliminar(DeleteView):
    model = User
    template_name = 'donador/donador_borrar.html'
    success_url = reverse_lazy('lista_donante')

