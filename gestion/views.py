from django.shortcuts import render
from .models import Cliente

def home(request):
    return render(request, 'base.html')

def lista_clientes(request):
    # Traemos todos los clientes de la base de datos
    clientes = Cliente.objects.all()
    # Los pasamos a la plantilla en un diccionario llamado 'contexto'
    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes})