from django.urls import path , include
from . import views
from .views import ClienteUpdateView , ProductoUpdateView



urlpatterns = [
    path('crear_usuario/',views.Crear_usuario,name='crear_usuario'),
    path('consultar_usuario/', views.consultar_usuario,name='consultar_usuario'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('consultar_producto/', views.consultar_producto, name='consultar_producto'),
    path('producto/<int:pk>/editar/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('consultar_venta/<int:venta_id>/', views.consultar_venta, name='consultar_venta'),
    path('crear_venta/', views.crear_venta, name='crear_venta'),

    # crud para empleado

    # crud de pago
    path('consultar_venta/<int:venta_id>/pdf/', views.consultar_venta_pdf, name='consultar_venta_pdf'),

    # crud de pago
    path('agregar_pago/', views.registrar_pago, name='agregar_pago'),
    path('consultar_pago/', views.mostrar_pagos, name='consultar_pago'),
    path('venta/<int:venta_id>/', views.eliminar_pago, name='eliminar_pago'),


]