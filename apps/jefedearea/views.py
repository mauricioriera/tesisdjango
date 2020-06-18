from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from apps.jefedearea.forms import RegistroForm, JefedeAreaForm,ModificarForm
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.models import User, Group
from apps.jefedearea.models import JefedeArea


class preperfil(ListView):
    model: JefedeArea
    template_name = 'jefedearea/jefedearea_preprofile.html'

    def get_queryset(self, *args, **kwargs):
        return JefedeArea.objects.filter(user=self.request.user)


def perfil(request, pk):
    j = JefedeArea.objects.get(pk=pk)
    return render(request, 'jefedearea/jefedearea_profile.html', {'jefedearea': j})


class JefedeAreaCrear(AccessMixin,CreateView):
    model = JefedeArea
    form_class = JefedeAreaForm
    second_form_class = RegistroForm
    template_name = 'jefedearea/jefedearea_add.html'
    success_url = reverse_lazy('jefedearea_listar')

    def get_context_data(self, **kwargs):
        context = super(JefedeAreaCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            jefedearea = form.save(commit=False)
            jefedearea.user = form2.save()
            jefedearea.save()
            g = Group.objects.get(name='Jefe de Área')
            g.user_set.add(jefedearea.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request,self.template_name, {'form':form,'form2':form2})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name__in=['Donantes','Empleado','Jefe de Área']).exists():
            return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)


class JefedeAreaLista(AccessMixin,ListView):
    model = JefedeArea
    template_name = 'jefedearea/jefedearea_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name__in=['Donantes','Empleado','Jefe de Área']).exists():
            return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)


class JefedeAreaBorrar(AccessMixin,DeleteView):
    model = User
    template_name = 'jefedearea/jefedearea_delete.html'
    success_url = reverse_lazy('jefedearea_listar')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name__in=['Donantes','Empleado','Jefe de Área']).exists():
            return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)


class JefedeAreaModificar(AccessMixin,UpdateView):
    model = JefedeArea
    second_model = User
    form_class = JefedeAreaForm
    second_form_class = ModificarForm
    template_name = 'jefedearea/jefedearea_update.html'
    success_url = reverse_lazy('empleado_listar')

    def get_context_data(self, **kwargs):
        context = super(JefedeAreaModificar, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        jefedearea = self.model.objects.get(id=pk)
        user = self.second_model.objects.get(id=jefedearea.user_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=user)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_jefedearea = kwargs['pk']
        jefedearea = self.model.objects.get(id=id_jefedearea)
        user = self.second_model.objects.get(id=jefedearea.user_id)
        form2 = self.second_form_class(request.POST, instance=user)
        form = self.form_class(request.POST, instance=jefedearea)
        if form.is_valid() and form2.is_valid():
            form2.save()
            form.save()
            g = Group.objects.get(name="Jefe de Área")
            g.user_set.add(jefedearea.user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name__in=['Donantes','Empleado']).exists():
            return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)