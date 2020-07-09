"""latesi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from .views import inicio, validacion, logout, errorpage
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout, name='cerrar_sesion'),
    path('validar/', validacion,name='validar_usuario'),
    path('empleado/', include('apps.empleado.urls'), name='empleado'),
    path('donador/', include('apps.donador.urls'), name='donador'),
    path('hospital/', include('apps.hospital.urls'),name='hospital'),
    path('jefedearea/',include('apps.jefedearea.urls'),name='jefedearea'),
    path('donacion/',include('apps.donacion.urls'),name='donacion'),
    path('error/',login_required(errorpage),name='pagina_error'),
    path('reset/password_reset', PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                                           html_email_template_name='registration/password_reset_email.html',email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('reset/password_reset_done',
         PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-za-z_\-]+)/(?P<token>.+)/$',
            PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
            name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete')

]
