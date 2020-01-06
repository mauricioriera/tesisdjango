from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from apps.empleado.forms import EmpleadoForm, RegistroForm
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from apps.empleado.models import Empleado
from django.contrib.auth.models import User, Group



class preperfil(ListView):
    model: Empleado
    template_name = 'empleado/preperfil.html'

    def get_queryset(self, *args, **kwargs):
        return Empleado.objects.filter(user=self.request.user)

def perfil (request,pk):
    e = Empleado.objects.get(pk=pk)
    return render(request, 'empleado/perfil.html', {'empleado': e})


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
            g = Group.objects.get(name= empleado.groups)
            g.user_set.add(empleado.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))


class EmpleadoLista(ListView):
    model = Empleado
    template_name = 'empleado/empleado_list.html'


class EmpleadoBorrar(DeleteView):
    model = User
    template_name = 'empleado/empleado_delete.html'
    success_url = reverse_lazy('empleado_listar')

    @method_decorator(permission_required('empleado.delete_empleado', reverse_lazy('empleado_listar')))
    def dispatch(self, *args, **kwargs):
        return super(EmpleadoBorrar, self).dispatch(*args, **kwargs)


class EmpleadoModificar(UpdateView):
    model = Empleado
    second_model = User
    form_class = EmpleadoForm
    second_form_class = RegistroForm
    template_name = 'empleado/empleado_formulario.html'
    success_url = reverse_lazy('empleado_listar')

    def get_context_data(self, **kwargs):
        context = super(EmpleadoModificar, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        empleado =self.model.objects.get(id=pk)
        user =self.second_model.objects.get(id=empleado.user_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=user)
        context['id'] =pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_empleado = kwargs['pk']
        empleado = self.model.objects.get(id=id_empleado)
        user = self.second_model.objects.get(id=empleado.user_id)
        form2 = self.second_form_class(request.POST, instance=user)
        form = self.form_class(request.POST, instance=empleado)
        if form.is_valid() and form2.is_valid():
            form2.save()
            form.save()
            g = Group.objects.get(name=empleado.groups)
            g.user_set.add(empleado.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())