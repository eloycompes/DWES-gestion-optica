import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # <--- Este es el IMPORT CORRECTO
from django.db.models import Q
from django.db import transaction

# Tus modelos y formularios
from .forms import EncargoForm, GraduacionForm, ConsultaForm, VentaRapidaForm
from .models import Consulta, Cliente, DetallePedido, Graduacion, Producto, Pedido

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
    cliente = get_object_or_404(Cliente, id=cliente_id)
    # Traemos los pedidos de este cliente, del más reciente al más antiguo
    pedidos = Pedido.objects.filter(cliente=cliente).order_by('-fecha')
    
    return render(request, 'gestion/detalle_cliente.html', {
        'cliente': cliente,
        'pedidos': pedidos  # <--- Enviamos los pedidos a la web
    })

def detalle_consulta(request, consulta_id):
    # Obtenemos la consulta
    consulta = get_object_or_404(Consulta, id=consulta_id)
    # Intentamos obtener la graduación vinculada (si existe)
    try:
        graduacion = consulta.graduacion
    except Graduacion.DoesNotExist:
        graduacion = None
        
    return render(request, 'gestion/detalle_consulta.html', {
        'consulta': consulta,
        'graduacion': graduacion
    })

def lista_pedidos(request):
    # Por ahora solo devolvemos un texto simple
    from django.http import HttpResponse
    return HttpResponse("Aquí se verá el listado de pedidos")

def registrar_graduacion(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    graduacion_instancia = getattr(consulta, 'graduacion', None)

    if request.method == 'POST':
        form = GraduacionForm(request.POST, instance=graduacion_instancia)
        if form.is_valid():
            graduacion = form.save(commit=False)
            # Unimos los campos aquí antes de guardar
            graduacion.od_queratometria = f"{form.cleaned_data['od_q1']} x {form.cleaned_data['od_q2']}"
            graduacion.oi_queratometria = f"{form.cleaned_data['oi_q1']} x {form.cleaned_data['oi_q2']}"
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


def venta_rapida(request):
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        form = VentaRapidaForm(request.POST)
        # Recogemos los datos ocultos que creó el JavaScript
        productos_ids = request.POST.getlist('prod_id_real[]')
        cantidades = request.POST.getlist('cant[]')

        if form.is_valid():
            if not productos_ids:
                messages.error(request, "No has añadido ningún producto al carrito.")
            else:
                try:
                    with transaction.atomic():
                        # 1. Creamos la cabecera del Pedido
                        pedido = form.save(commit=False)
                        pedido.total_importe = 0  # Se calculará ahora
                        pedido.save()

                        total_acumulado = 0

                        # 2. Creamos cada línea de detalle
                        for p_id, cantidad in zip(productos_ids, cantidades):
                            producto = Producto.objects.get(id=p_id)
                            cant = int(cantidad)

                            # Verificamos stock
                            if producto.stock < cant:
                                raise ValueError(f"Stock insuficiente para {producto.nombre}")

                            # Crear línea de venta
                            DetallePedido.objects.create(
                                pedido=pedido,
                                producto=producto,
                                cantidad=cant,
                                precio_unitario=producto.precio
                            )

                            # Actualizar stock del producto
                            producto.stock -= cant
                            producto.save()

                            total_acumulado += (producto.precio * cant)

                        # 3. Guardamos el total final en el pedido
                        pedido.total_importe = total_acumulado
                        pedido.save()

                    messages.success(request, f"Venta {pedido.id} realizada con éxito. Total: {total_acumulado}€")
                    return redirect('venta_rapida')

                except Exception as e:
                    messages.error(request, f"Error en la venta: {e}")
    else:
        form = VentaRapidaForm()

    return render(request, 'gestion/venta_rapida.html', {
        'form': form,
        'productos': productos
    })


def nuevo_encargo(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        # Pasamos el cliente al formulario para la validación y el filtrado
        form = EncargoForm(request.POST, cliente=cliente)
        if form.is_valid():
            encargo = form.save(commit=False)
            encargo.cliente = cliente
            encargo.save()
            messages.success(request, f"Encargo creado correctamente para {cliente.nombre}")
            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        # Al cargar la página, pasamos el cliente para que el combo de graduaciones se filtre
        form = EncargoForm(cliente=cliente)
    
    return render(request, 'gestion/nuevo_encargo.html', {
        'form': form,
        'cliente': cliente
    })