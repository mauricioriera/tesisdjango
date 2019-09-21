from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from apps.empleado.forms import EmpleadoForm, RegistroForm
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from apps.empleado.models import Empleado
from django.contrib.auth.models import User


def validacion(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 0:
            return redirect('empleado_listar')
        elif request.user.is_superuser == 1:
            return redirect('empleado_crear')
    return redirect('login')

class EmpleadoCrear(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    second_form_class = RegistroForm
    template_name = 'empleado/empleado_formulario.html'
    success_url = reverse_lazy('empleado_listar')

    def get_context_data(self, **kwargs):
        context = super(EmpleadoCrear, self).get_context_data(**kwargs)
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
            empleado = form.save(commit=False)
            empleado.user = form2.save()
            empleado.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class EmpleadoLista(ListView):
    model = Empleado
    template_name = 'empleado/empleado_list.html'

class EmpleadoBorrar(DeleteView):
    model = Empleado
    template_name = 'empleado/empleado_delete.html'
    success_url = reverse_lazy('empleado_listar')

class EmpleadoModificar(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado/empleado_formulario.html'
    success_url = reverse_lazy('empleado_listar')