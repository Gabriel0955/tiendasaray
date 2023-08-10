from django.urls import path,include

import Inventario.views
from . import views
from django.conf.urls.static import static
from django.conf import settings
from Inventario.views import consultar_usuario




urlpatterns = [

    path('g/',views.mi_vista, name='mi_vista'),
    path('',Inventario.views.consultar_usuario,name='consultar')

]