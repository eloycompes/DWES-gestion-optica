from django.shortcuts import render
from .models import Cliente, Consulta
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'base.html')

def lista_clientes(request):
    # Traemos todos los clientes de la base de datos
    clientes = Cliente.objects.all()
    # Los pasamos a la plantilla en un diccionario llamado 'contexto'
    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes})

def detalle_consulta(request, consulta_id):
    # Buscamos la consulta por su ID o devolvemos un error 404 si no existe
    consulta = get_object_or_404(Consulta, id=consulta_id)
    # Como es una relación OneToOne, accedemos a la graduación desde la consulta
    return render(request, 'gestion/detalle_consulta.html', {'consulta': consulta})

from .models import Pedido # Añade Pedido a tus imports

def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha') # Los más nuevos primero
    return render(request, 'gestion/lista_pedidos.html', {'pedidos': pedidos})