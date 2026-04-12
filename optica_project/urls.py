from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('consulta/<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
]