from django.shortcuts import render
from .models import Cliente, Consulta
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'base.html')

def lista_clientes(request):
    query = request.GET.get('q') # Capturamos lo que el usuario escribe
    if query:
        # Filtramos por nombre, apellidos o DNI
        from django.db.models import Q
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | 
            Q(apellidos__icontains=query) | 
            Q(dni__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()
    
    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes, 'query': query})

def detalle_consulta(request, consulta_id):
    # Buscamos la consulta por su ID o devolvemos un error 404 si no existe
    consulta = get_object_or_404(Consulta, id=consulta_id)
    # Como es una relación OneToOne, accedemos a la graduación desde la consulta
    return render(request, 'gestion/detalle_consulta.html', {'consulta': consulta})

from .models import Pedido # Añade Pedido a tus imports

def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha') # Los más nuevos primero
    return render(request, 'gestion/lista_pedidos.html', {'pedidos': pedidos})

def detalle_cliente(request, cliente_id):
    # Obtenemos el cliente y todas sus consultas asociadas
    cliente = get_object_or_404(Cliente, id=cliente_id)
    consultas = cliente.consulta_set.all().order_by('-fecha')
    return render(request, 'gestion/detalle_cliente.html', {
        'cliente': cliente,
        'consultas': consultas
    })