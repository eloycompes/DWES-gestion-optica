from django.urls import path
from . import views

urlpatterns = [
    # Clientes
    path('', views.lista_clientes, name='lista_clientes'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('cliente/<int:cliente_id>/nueva-consulta/', views.crear_consulta, name='crear_consulta'),
    
    # Consultas
    path('consulta/<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta'),
    path('consulta/<int:consulta_id>/graduacion/', views.registrar_graduacion, name='registrar_graduacion'),
    
    # Pedidos
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),

    # Venta rápida
    path('venta-rapida/', views.venta_rapida, name='venta_rapida'),
]