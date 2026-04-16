from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio
    path('', views.home, name='home'),

    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('cliente/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('cliente/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Consultas
    path('consulta/<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta'),
    path('consulta/<int:consulta_id>/graduacion/', views.registrar_graduacion, name='registrar_graduacion'),
    path('cliente/<int:cliente_id>/nueva-consulta/', views.crear_consulta, name='crear_consulta'),

    # Venta rápida
    path('venta-rapida/', views.venta_rapida, name='venta_rapida'),

    # Encargo
    path('cliente/<int:cliente_id>/nuevo-encargo/', views.nuevo_encargo, name='nuevo_encargo'),
    path('encargo/<int:encargo_id>/pagar/', views.marcar_pagado, name='marcar_pagado'),
    path('encargo/<int:encargo_id>/entregar/', views.entregar_encargo, name='entregar_encargo'),
    path('encargo/<int:encargo_id>/editar/', views.editar_encargo, name='editar_encargo'),
    path('encargo/eliminar/<int:encargo_id>/', views.eliminar_encargo, name='eliminar_encargo'),

    # Citas
    path('agenda/', views.agenda, name='agenda'),
    path('cita/nueva/', views.nueva_cita, name='nueva_cita'),
    path('cliente/<int:cliente_id>/nueva-cita/', views.nueva_cita, name='nueva_cita_cliente'),
    path('cita/<int:cita_id>/estado/<str:nuevo_estado>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
]