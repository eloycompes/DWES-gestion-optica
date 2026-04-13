from django.shortcuts import render, redirect, get_object_or_404
from .forms import GraduacionForm, ConsultaForm
from .models import Consulta, Cliente, Graduacion
from django.db.models import Q

def lista_clientes(request):
    query = request.GET.get('q', '')
    if query:

        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | 
            Q(apellidos__icontains=query) | 
            Q(dni__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()
    
    return render(request, 'gestion/lista_clientes.html', {
        'clientes': clientes,
        'query': query
    })

def detalle_cliente(request, cliente_id):

    cliente = Cliente.objects.get(id=cliente_id)
    return render(request, 'gestion/detalle_cliente.html', {'cliente': cliente})

def detalle_consulta(request, consulta_id):
    # Por ahora solo devolvemos un texto simple para que no de error
    from django.http import HttpResponse
    return HttpResponse(f"Aquí se verá la consulta con ID {consulta_id}")

def lista_pedidos(request):
    # Por ahora solo devolvemos un texto simple
    from django.http import HttpResponse
    return HttpResponse("Aquí se verá el listado de pedidos")

def registrar_graduacion(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Intentamos obtener la graduación si ya existe
    try:
        graduacion_instancia = consulta.graduacion
    except Graduacion.DoesNotExist:
        graduacion_instancia = None

    if request.method == 'POST':
        # Si existe, le pasamos la 'instance' para que Django haga un UPDATE y no un INSERT
        form = GraduacionForm(request.POST, instance=graduacion_instancia)
        if form.is_valid():
            graduacion = form.save(commit=False)
            graduacion.consulta = consulta
            graduacion.save()
            return redirect('detalle_cliente', cliente_id=consulta.cliente.id)
    else:
        # Cargamos el formulario con los datos existentes si los hay
        form = GraduacionForm(instance=graduacion_instancia)
    
    return render(request, 'gestion/form_graduacion.html', {
        'form': form,
        'consulta': consulta
    })

def crear_consulta(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.cliente = cliente
            # ASIGNAMOS EL USUARIO ACTUAL COMO ÓPTICO
            # Nota: Esto asume que el usuario tiene un perfil de óptico o es el admin
            if request.user.is_authenticated:
                consulta.optico = request.user 
            
            consulta.save()
            return redirect('registrar_graduacion', consulta_id=consulta.id)
    else:
        form = ConsultaForm()
    
    return render(request, 'gestion/form_consulta.html', {'form': form, 'cliente': cliente})