from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView
from apps.donacion.models import Donacion
from apps.donacion.forms import DonacionForm


class DonacionCrear (AccessMixin,CreateView):
    model = Donacion
    form_class = DonacionForm
    template_name = 'donacion/registrodonacion.html'
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.groups.filter(name__in=['Donantes', 'Empleado']).exists():
            return redirect('pagina_error')
        return super().dispatch(request, *args, **kwargs)

