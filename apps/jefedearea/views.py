
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from apps.jefedearea.forms import RegistroForm, JefedeAreaForm,ModificarForm
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.models import User, Group
from apps.jefedearea.models import JefedeArea
from apps.donador.models import Donador
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from datetime import datetime as date
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import A4


from django.http import HttpResponse
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from reportlab.platypus import Table


def reporte(request,):

    cant_donantes=Donador.objects.all().count()
    nombre=(date.now().strftime('reporte %d-%m-%y %H.%M.%S.pdf'))
    with PdfPages(nombre) as pdf:
        genero=[Donador.objects.filter(genero='M').count(), Donador.objects.filter(genero='F').count()]
        cuenta=[(genero[0]*100)/cant_donantes,(genero[1]*100)/cant_donantes]
        labels=["Hombres","Mujeres"]
        two=[f"{cuenta[0]}% = {genero[0]}",f"{cuenta[1]}% = {genero[1]}"]
        colors=['yellow', 'red']
        plt.title('REPORTE DONANTES')
        plt.suptitle("cantidad de donantes ", x=0.52, y=0.89,)
        plt.pie(genero, colors=colors, autopct='%1.2f %%')
        first_legend=plt.legend(labels, loc="upper right")
        plt.gca().add_artist(first_legend)
        plt.legend(two, loc="lower right")
        plt.axis('equal')
        pdf.savefig()
        plt.close()
        plt.title('Cantidad de donantes \n segun rango de edad')
        edadh=[(d.calcularEdad) for d in Donador.objects.filter(genero='M')]
        edadm=[(d.calcularEdad) for d in Donador.objects.filter(genero='F')]
        lista1=[]
        lista2=[]
        lista3=[]
        lista4=[]
        lista5=[]
        lista6=[]
        lista7=[]
        lista8=[]
        for i in edadh:
            if i>=18 and i<=30:
                lista1.append(i)
            elif i>30 and i<+40:
                lista2.append(i)
            elif i>40 and i<=50:
                lista3.append(i)
            else:
                lista4.append(i)
        for i in edadm:
            if i>=18 and i<=30:
                lista5.append(i)
            elif i>30 and i<+40:
                lista6.append(i)
            elif i>40 and i<=50:
                lista7.append(i)
            else:
                lista8.append(i)
        edadesh=[len(lista1),len(lista2),len(lista3),len(lista4)]
        edadesm=[len(lista5),len(lista6),len(lista7),len(lista8)]
        labels=[('18-30'),('31-40'),('41-50'),('51-65')]
        ind=np.arange(4)
        width=0.35
        p1 = plt.bar(ind, edadesh, width, color="blue")
        p2 = plt.bar(ind, edadesm, width,color="red",bottom=edadesh)
        plt.ylabel('cantidad de personas')
        plt.xticks(ind,labels)
        plt.yticks(np.arange(0, 10, 1))
        plt.legend((p1[0], p2[0]), ('Hombres', 'Mujeres'))
        pdf.savefig()
        plt.close()
        plt.title('Cantidad de donantes \n segun grupo y factor')
        grupo=[Donador.objects.filter(grupo_sanguineo='A',factor_sanguineo='+').count(),Donador.objects.filter(grupo_sanguineo='A',factor_sanguineo='-').count(),
               Donador.objects.filter(grupo_sanguineo='B', factor_sanguineo='+').count(),Donador.objects.filter(grupo_sanguineo='B',factor_sanguineo='-').count(),
               Donador.objects.filter(grupo_sanguineo='0', factor_sanguineo='+').count(),Donador.objects.filter(grupo_sanguineo='0',factor_sanguineo='-').count(),
               Donador.objects.filter(grupo_sanguineo='AB', factor_sanguineo='+').count(),Donador.objects.filter(grupo_sanguineo='AB',factor_sanguineo='-').count()]
        labels=[" A+ "," A- "," B+ "," B- "," 0+ "," 0- "," AB+ "," AB- "]
        plt.bar(range(8),grupo, edgecolor='black')
        plt.xticks(range(8),labels)
        plt.xlabel('Grupo/Factor')
        plt.ylabel('Cantidad de Persona')
        pdf.savefig()
        plt.close()
        plt.suptitle('Cantidad de donantes \n activos')
        activos=[Donador.objects.filter(activo=True).count(),Donador.objects.filter(activo=False).count()]
        cuenta=[(activos[0]*100)/cant_donantes,(activos[1]*100)/cant_donantes]
        labels=["Activos", "No activos"]
        two = [f"{cuenta[0]}% = {activos[0]}", f"{cuenta[1]}% = {activos[1]}"]
        colors=["green",'red']
        plt.pie(activos, colors=colors, autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '')
        first_legend = plt.legend(labels, loc="upper right")
        plt.gca().add_artist(first_legend)
        plt.legend(two, loc="lower right")
        plt.axis('equal')
        pdf.savefig()
        plt.close()
        return redirect('inicio')

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

    '''@method_decorator(permission_required('donador.view_jefedearea', reverse_lazy('preperfil_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaLista, self).dispatch(*args, **kwargs)

    @method_decorator(permission_required('empleado.view_jefedearea', reverse_lazy('lista_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaLista, self).dispatch(*args, **kwargs)'''


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

    '''@method_decorator(permission_required('donador.update_jefedearea', reverse_lazy('preperfil_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaModificar, self).dispatch(*args, **kwargs)

    @method_decorator(permission_required('empleado.update_jefedearea', reverse_lazy('lista_donante')))
    def dispatch(self, *args, **kwargs):
        return super(JefedeAreaModificar, self).dispatch(*args, **kwargs)'''