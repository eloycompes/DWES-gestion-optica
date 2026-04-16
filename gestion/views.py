import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # <--- Este es el IMPORT CORRECTO
from django.db.models import Q
from django.db import transaction
from django.utils import timezone

# Tus modelos y formularios
from .forms import CitaForm, ClienteForm, EncargoForm, GraduacionForm, ConsultaForm, VentaRapidaForm
from .models import Cita, Consulta, Cliente, DetallePedido, Encargo, Graduacion, Producto, Pedido

def home(request):
    return render(request, 'gestion/home.html')

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = ClienteForm()
    return render(request, 'gestion/form_cliente.html', {'form': form, 'editando': False})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('detalle_cliente', cliente_id=cliente.id)
        # Si NO es válido, el código sigue hacia abajo y vuelve a renderizar el form con los errores
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'gestion/form_cliente.html', {
        'form': form, 
        'editando': True,
        'cliente': cliente # Opcional, para el título
    })

def eliminar_cliente(request, cliente_id):
    """Vista para borrar un cliente"""
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.delete()
        return redirect('lista_clientes')
    return redirect('detalle_cliente', cliente_id=cliente_id)

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
    
    return render(request, 'gestion/detalle_cliente.html', {
        'cliente': cliente,
        'consultas': cliente.consultas.all().order_by('-fecha'),
        'encargos_activos': cliente.encargos.exclude(estado='ENT').order_by('-id'),
        'historial_encargos': cliente.encargos.filter(estado='ENT').order_by('-id'),
        'ventas_rapidas': cliente.ventas_rapidas.all().order_by('-fecha'),
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
    # Traemos todas las monturas para el buscador
    monturas_db = Producto.objects.filter(categoria__nombre__iexact="Monturas")
    
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
        'cliente': cliente,
        'monturas_db': monturas_db # <--- Enviamos la lista
    })

def editar_encargo(request, encargo_id):
    encargo = get_object_or_404(Encargo, id=encargo_id)
    cliente_id = encargo.cliente.id 
    
    # IMPORTANTE: Necesitamos enviar las monturas para que el datalist del HTML se llene
    monturas_db = Producto.objects.filter(categoria__nombre="Monturas")
    
    if request.method == 'POST':
        form = EncargoForm(request.POST, instance=encargo, cliente=encargo.cliente)
        if form.is_valid():
            form.save()
            return redirect('detalle_cliente', cliente_id=cliente_id)
    else:
        form = EncargoForm(instance=encargo, cliente=encargo.cliente)
    
    return render(request, 'gestion/nuevo_encargo.html', {
        'form': form,
        'cliente': encargo.cliente,
        'editando': True,
        'monturas_db': monturas_db  # <--- ESTA LÍNEA ES LA QUE FALTA
    })

def marcar_pagado(request, encargo_id):
    encargo = get_object_or_404(Encargo, id=encargo_id)
    encargo.pagado = True
    encargo.save()
    # Redirigimos al expediente del cliente al que pertenece el encargo
    return redirect('detalle_cliente', cliente_id=encargo.cliente.id)

def entregar_encargo(request, encargo_id):
    if request.method == 'POST':
        encargo = get_object_or_404(Encargo, id=encargo_id)
        
        # SEGURIDAD: Solo restamos stock si el encargo NO estaba entregado ya
        if encargo.estado != 'ENT':
            sku_buscado = encargo.montura_marca_modelo
            producto = Producto.objects.filter(codigo=sku_buscado).first()
            if not producto:
                producto = Producto.objects.filter(nombre=sku_buscado).first()

            if producto and producto.stock > 0:
                producto.stock -= 1
                producto.save()
            
            # Actualizamos a entregado
            encargo.estado = 'ENT'
            encargo.save()
        
        return redirect('detalle_cliente', cliente_id=encargo.cliente.id)
    return redirect('lista_clientes')

def eliminar_encargo(request, encargo_id):
    if request.method == 'POST':
        encargo = get_object_or_404(Encargo, id=encargo_id)
        
        # SEGURIDAD: Si está pagado, prohibimos borrar desde aquí
        if encargo.pagado:
            # Opcional: puedes mandar un mensaje de error
            from django.contrib import messages
            messages.error(request, "No se puede eliminar un encargo que ya ha sido pagado.")
            return redirect('detalle_cliente', cliente_id=encargo.cliente.id)
            
        cliente_id = encargo.cliente.id
        encargo.delete()
        return redirect('detalle_cliente', cliente_id=cliente_id)
    
    return redirect('lista_clientes')

def agenda(request):
    # Mostramos las citas desde hoy en adelante, ordenadas por fecha
    citas = Cita.objects.filter(fecha_hora__gte=timezone.now()).order_by('fecha_hora')
    return render(request, 'gestion/agenda.html', {'citas': citas})

def nueva_cita(request, cliente_id=None):
    cliente = None
    if cliente_id:
        cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            if cliente:
                cita.cliente = cliente
            cita.save()
            return redirect('agenda')
    else:
        # Si venimos de la ficha del cliente, lo pasamos como valor inicial
        form = CitaForm(initial={'cliente': cliente}) if cliente else CitaForm()

    return render(request, 'gestion/form_cita.html', {'form': form, 'cliente': cliente})

def cambiar_estado_cita(request, cita_id, nuevo_estado):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.estado = nuevo_estado
    cita.save()
    return redirect('agenda')