from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from apps.donador.forms import DonadorForm, RegistroForm, ModificarForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from apps.donador.models import Donador
from django.contrib.auth.models import Group, User



def perfil (request, pk):
    d = Donador.objects.get(pk=pk)
    donante= request.user.groups.filter(name='Donantes').exists()
    return render(request, 'donador/perfil.html', {'donador': d ,'donante': donante})


def activacion(request,pk):
    donador = get_object_or_404(Donador, pk=pk)
    if request.user.groups.filter(name='Donantes').exists():
        return redirect('lista_donante')
    else:
        if donador.activo == False:
            donador.activo = True
            donador.save()
        else:
            donador.activo = False
            donador.save()
    return redirect('lista_donante')


class preperfil (ListView):
    model = Donador
    template_name = "donador/preperfil.html"

    def get_queryset(self, *args, **kwargs):
        return Donador.objects.filter(user=self.request.user)


class DonadorCrear(CreateView):
    model = Donador
    form_class = DonadorForm
    second_form_class = RegistroForm
    template_name = 'donador/registro.html'
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.session.is_empty() and self.request.user.groups.filter(name='Donantes').exists():
            return redirect(reverse_lazy('preperfil_donante'))
        return super(DonadorCrear, self).dispatch(request,*args,**kwargs)

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
    queryset = Donador.objects.order_by('-activo')

    def get_queryset(self):
        queryset = super(DonadorLista, self).get_queryset()
        filter1 = self.request.GET.get("grupo")
        filter2 = self.request.GET.get("factor")
        if filter1 == 'A' or filter1 == 'B' or filter1 == 'AB' or filter1 == '0':
            queryset = queryset.filter(grupo_sanguineo=str(filter1))
        if filter2 == '+' or filter2 == '-':
            queryset = queryset.filter(factor_sanguineo=str(filter2))
        return queryset

    @method_decorator(permission_required('donador.view_donador', reverse_lazy('preperfil_donante')))
    def dispatch(self, *args, **kwargs):
        return super(DonadorLista, self).dispatch(*args, **kwargs)


class DonadorModificar(UpdateView):
    model = Donador
    second_model = User
    form_class = DonadorForm
    second_form_class = ModificarForm
    template_name = 'donador/donador_update.html'
    success_url = reverse_lazy('preperfil_donante')

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
            if self.request.user.groups.filter(name='Empleado').exists() or self.request.user.groups.filter(name='Jefe de Área').exists():
                return HttpResponseRedirect(reverse_lazy('lista_donante'))
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

class DonadorEliminar(DeleteView):
    model = User
    template_name = 'donador/donador_borrar.html'
    success_url = reverse_lazy('lista_donante')