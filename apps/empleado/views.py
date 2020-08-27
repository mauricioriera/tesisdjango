from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.empleado.forms import EmpleadoForm, RegistroForm,ModificarForm
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from apps.empleado.models import Empleado
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import AccessMixin


class preperfil(ListView):
    model: Empleado
    template_name = 'empleado/empleado_preprofile.html'

    def get_queryset(self, *args, **kwargs):
        return Empleado.objects.filter(user=self.request.user)


def perfil (request,pk):
    e = Empleado.objects.get(pk=pk)
    return render(request, 'empleado/empleado_profile.html', {'empleado': e})


class EmpleadoCrear(AccessMixin,CreateView):
    model = Empleado
    form_class = EmpleadoForm
    second_form_class = RegistroForm
    template_name = 'empleado/empleado_add.html'
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
            g = Group.objects.get(name='Empleado')
            g.user_set.add(empleado.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request,self.template_name, {'form':form,'form2':form2})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Jefe de Área").exists():
           return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)


class EmpleadoLista(AccessMixin,ListView):
    model = Empleado
    template_name = 'empleado/empleado_list.html'
    paginate_by = 3


    def get_queryset(self):
        queryset = super(EmpleadoLista, self).get_queryset()
        filtro = self.request.GET.get("filtro")
        if filtro:
            queryset =queryset.filter(user__last_name__icontains=filtro) | queryset.filter(user__first_name__icontains=filtro) | queryset.filter(numero_legajo__icontains=filtro)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Jefe de Área").exists():
           return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)


class EmpleadoBorrar(AccessMixin,DeleteView):
    model = User
    template_name = 'empleado/empleado_delete.html'
    success_url = reverse_lazy('empleado_listar')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Jefe de Área").exists():
           return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)


class EmpleadoModificar(AccessMixin,UpdateView):
    model = Empleado
    second_model = User
    form_class = EmpleadoForm
    second_form_class = ModificarForm
    template_name = 'empleado/empleado_update.html'
    success_url = reverse_lazy('preperfil_empleado')

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
            g = Group.objects.get(name="Empleado")
            g.user_set.add(empleado.user)
            if self.request.user.groups.filter(name='Jefe de Área').exists():
                return HttpResponseRedirect(reverse_lazy('empleado_listar'))
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name="Donantes").exists():
           return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)