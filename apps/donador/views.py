from django.contrib.auth.mixins import AccessMixin
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from apps.donador.forms import DonadorForm, RegistroForm, ModificarForm, DesactivarForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from apps.donador.models import Donador, Desactivar
from apps.jefedearea.models import JefedeArea
from apps.empleado.models import Empleado
from django.contrib.auth.models import Group, User
from threading import Thread
from urllib import parse
from django.contrib import messages
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.db import connection

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')

@register_job(scheduler, 'interval', hours=24)
def mujeractivarmotivodonosangre():
    cursor = connection.cursor()
    cursor.execute('''UPDATE tesisnueva.donador_donador as dd1 
                        SET dd1.activo=1 where dd1.genero='F' and
                        dd1.activo=0 and 
                        (SELECT date_add(fecha_desactivar,INTERVAL 120 day)
                        FROM tesisnueva.donador_desactivar ds
                        where ds.motivo=1 and
                        ds.donador_id= dd1.id
                        order by fecha_desactivar desc 
                        limit 1)''')
@register_job(scheduler, 'interval', hours=24)
def hombreactivarmotivodonosangre():
    cursor = connection.cursor()
    cursor.execute('''UPDATE tesisnueva.donador_donador as dd1 
                        SET dd1.activo=1 where dd1.genero='M' and
                        dd1.activo=0 and 
                        (SELECT date_add(fecha_desactivar,INTERVAL 90 day)
                        FROM tesisnueva.donador_desactivar ds
                        where ds.motivo=1 and
                        ds.donador_id= dd1.id
                        order by fecha_desactivar desc 
                        limit 1)''')
@register_job(scheduler, 'interval', hours=24)
def mujeractivarmotivoembarazo():
    cursor = connection.cursor()
    cursor.execute('''UPDATE tesisnueva.donador_donador as dd1 
                            SET dd1.activo=2 and
                            dd1.activo=0 and 
                            (SELECT date_add(fecha_desactivar,INTERVAL 450 day)
                            FROM tesisnueva.donador_desactivar ds
                            where ds.motivo=1 and
                            ds.donador_id= dd1.id
                            order by fecha_desactivar desc 
                            limit 1)''')
register_events(scheduler)
scheduler.start()


def enviarmail(request, pk):
    d = Donador.objects.get(pk=pk)
    subject = 'DONAR SANGRE'
    message = 'mensaje'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [d.user.email]
    send_mail(subject, message, email_from, [recipient_list, ])


def hilo(request, pk):
    t = Thread(target=enviarmail, args=(request, pk))
    t.start()
    d = Donador.objects.get(pk=pk)
    messages.add_message(request, messages.SUCCESS, f'Se envio email a {d.user.username}')
    return redirect('{}?grupo={}&factor={}'.format(reverse('lista_donante'), request.session['grupo'],
                                                   parse.quote(request.session['factor'])))

def activacion(request, pk):
    donador = Donador.objects.get(pk=pk)
    if request.user.groups.filter(name='Donantes').exists():
        return redirect('pagina_error')
    donador.activo = not donador.activo
    donador.save()
    return redirect('lista_donante')


class Desactivar(CreateView):
    model = Desactivar
    form_class = DesactivarForm
    template_name = 'donante/donante_desactivar.html'
    success_url = reverse_lazy('lista_donante')

    def get(self, request, pk):
        d = Donador.objects.get(pk=pk)
        return render(request, 'donante/donante_desactivar.html', {'donador': d, 'form': self.form_class})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            desactivar = form.save(commit=False)
            if desactivar.motivo == 3 or desactivar.motivo == 4:
                desactivar.donador.user.delete()
                messages.add_message(request, messages.WARNING,
                         'usuario a sido eliminado por poseer enfermedad infeciosa o ser enfermo cronico')
            else:
                desactivar.save()
                donador = desactivar.donador
                donador.activo = False
                donador.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request, self.template_name, {'form': form})


def perfil(request, pk):
    d = Donador.objects.get(pk=pk)
    donante = request.user.groups.filter(name='Donantes').exists()
    return render(request, 'donante/donante_profile.html', {'donador': d, 'donante': donante})


class preperfil(ListView):
    model = Donador
    template_name = "donante/donante_preprofile.html"

    def get_queryset(self, *args, **kwargs):
        return Donador.objects.filter(user=self.request.user)


class DonadorCrear(CreateView):
    model = Donador
    form_class = DonadorForm
    second_form_class = RegistroForm
    template_name = 'donante/donante_add.html'
    success_url = reverse_lazy('inicio')

    def get_context_data(self, **kwargs):
        context = super(DonadorCrear, self).get_context_data(**kwargs)
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
            donador = form.save(commit=False)
            donador.user = form2.save()
            donador.save()
            g = Group.objects.get(name='Donantes')
            g.user_set.add(donador.user)
            messages.add_message(request, messages.SUCCESS, 'Su perfil se creo correctamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request, messages.ERROR, 'Su perfil no se pudo crear')
            return render(request, self.template_name, {'form': form, 'form2': form2})

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Donantes').exists():
            return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)


class DonadorLista(AccessMixin, ListView):
    template_name = 'donante/donante_list.html'
    queryset = Donador.objects.order_by('-activo')
    success_url = reverse_lazy('lista_donante')
    paginate_by = 5

    def get_queryset(self):
        queryset = super(DonadorLista, self).get_queryset()
        query = JefedeArea.objects.filter(user=self.request.user).distinct() or Empleado.objects.filter(
            user=self.request.user).distinct()
        for e in query:
            self.request.session['hospital'] = e.hospital.nombre

        filter1 = self.request.GET.get("grupo")
        filter2 = self.request.GET.get("factor")
        if filter1 == 'A' or filter1 == 'B' or filter1 == 'AB' or filter1 == '0':
            self.request.session['grupo'] = filter1
            queryset = queryset.filter(grupo_sanguineo=str(filter1))
        else:
            self.request.session['grupo'] = ''
        if filter2 == '+' or filter2 == '-':
            self.request.session['factor'] = filter2
            queryset = queryset.filter(factor_RH=str(filter2))
        else:
            self.request.session['factor'] = ''
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name='Donantes').exists():
            return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)


class DonadorModificar(UpdateView):
    model = Donador
    second_model = User
    form_class = DonadorForm
    second_form_class = ModificarForm
    template_name = 'donante/donante_update.html'
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
            if self.request.user.groups.filter(name='Empleado').exists() | self.request.user.groups.filter(
                    name='Jefe de Área').exists():
                messages.add_message(request, messages.SUCCESS, 'El perfil del donante se atualizo correctamente')
                return HttpResponseRedirect(reverse_lazy('lista_donante'))
            messages.add_message(request, messages.SUCCESS, 'Su perfil se actualizo correctamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request, messages.ERROR, 'Su perfil no se pudo actualizar')
            return HttpResponseRedirect(self.get_success_url())


class DonadorEliminar(DeleteView):
    model = User

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.groups.filter(name='Empleado').exists() | self.request.user.groups.filter(
                name='Jefe de Área').exists():
            return reverse('lista_donante')
        else:
            return reverse('inicio')