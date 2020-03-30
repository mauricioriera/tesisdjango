
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
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


class JefedeAreaCrear(CreateView):
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
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    @method_decorator(permission_required('donador.add_jefedearea', reverse_lazy('preperfil_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaCrear, self).dispatch(*args, **kwargs)

    @method_decorator(permission_required('empleado.add_jefedearea', reverse_lazy('lista_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaCrear, self).dispatch(*args, **kwargs)


class JefedeAreaLista(ListView):
    model = JefedeArea
    template_name = 'jefedearea/jefedearea_list.html'

    @method_decorator(permission_required('donador.view_jefedearea', reverse_lazy('preperfil_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaLista, self).dispatch(*args, **kwargs)

    @method_decorator(permission_required('empleado.view_jefedearea', reverse_lazy('lista_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaLista, self).dispatch(*args, **kwargs)


class JefedeAreaBorrar(DeleteView):
    model = User
    template_name = 'jefedearea/jefedearea_delete.html'
    success_url = reverse_lazy('jefedearea_listar')

    @method_decorator(permission_required('donador.delete_jefedearea', reverse_lazy('preperfil_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaBorrar, self).dispatch(*args, **kwargs)

    @method_decorator(permission_required('empleado.delete_jefedearea', reverse_lazy('lista_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaBorrar, self).dispatch(*args, **kwargs)


class JefedeAreaModificar(UpdateView):
    model = JefedeArea
    second_model = User
    form_class = JefedeAreaForm
    second_form_class = ModificarForm
    template_name = 'jefedearea/jefedearea_update.html'
    success_url = reverse_lazy('jefedearea_listar')

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

    @method_decorator(permission_required('donador.update_jefedearea', reverse_lazy('preperfil_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaModificar, self).dispatch(*args, **kwargs)

    @method_decorator(permission_required('empleado.update_jefedearea', reverse_lazy('lista_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaModificar, self).dispatch(*args, **kwargs)