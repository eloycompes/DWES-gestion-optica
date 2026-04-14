from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# 1. USUARIOS CON ROLES
class Usuario(AbstractUser):
    ROLES = (
        ('Admin', 'Administrador'),
        ('Director', 'Director'),
        ('Optico', 'Óptico'),
        ('Comercial', 'Comercial'),
        ('Cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='Optico')
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.rol})"

# 2. CLIENTES
class Cliente(models.Model):
    dni = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.dni}"

# 3. CITAS
class Cita(models.Model):
    ESTADOS = (
        ('Pendiente', 'Pendiente'),
        ('Finalizada', 'Finalizada'),
        ('Cancelada', 'Cancelada'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    optico = models.ForeignKey(Usuario, on_delete=models.PROTECT, limit_choices_to={'rol': 'Optico'})
    fecha_hora = models.DateTimeField()
    motivo_cita = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    def __str__(self):
        return f"Cita {self.cliente.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"

# 4. CONSULTA (ANAMNESIS)
class Consulta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='consultas')
    optico = models.ForeignKey(Usuario, on_delete=models.PROTECT, limit_choices_to={'rol': 'Optico'})
    fecha = models.DateField(auto_now_add=True)
    motivo = models.TextField()
    ant_medicos = models.TextField(blank=True)
    ant_oculares = models.TextField(blank=True)
    pantallas = models.CharField(max_length=100)
    gafas_sol = models.BooleanField(default=False)
    lentillas = models.BooleanField(default=False)
    recomendaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Consulta {self.cliente.nombre} ({self.fecha})"

# 5. GRADUACIÓN
class Graduacion(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='graduacion')
    
    # Ojo Derecho (OD)
    od_esfera = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    od_cilindro = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    od_eje = models.IntegerField(default=0)
    od_adicion = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    od_agudeza = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    
    # Ojo Izquierdo (OI)
    oi_esfera = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    oi_cilindro = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    oi_eje = models.IntegerField(default=0)
    oi_adicion = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    oi_agudeza = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    
    # Queratometría desglosada
    od_queratometria = models.CharField(max_length=100, blank=True, verbose_name="Queratometría OD")
    oi_queratometria = models.CharField(max_length=100, blank=True, verbose_name="Queratometría OI")
    
    # Tonometría desglosada (Presión intraocular)
    od_tonometria = models.IntegerField(null=True, blank=True, verbose_name="Tonometría OD")
    oi_tonometria = models.IntegerField(null=True, blank=True, verbose_name="Tonometría OI")

    biomicroscopio = models.TextField(blank=True)

    def __str__(self):
        return f"Graduación técnica - {self.consulta.cliente.nombre}"

# 6. FABRICANTE
class Fabricante(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# 7. PRODUCTO (Ajustado con Fabricante)
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código/SKU") # Campo para búsqueda rápida
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name="Categoría")
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE) # <-- Relación restaurada
    subcategoria = models.CharField(max_length=100, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"[{self.codigo}] {self.nombre}"

# 8. PEDIDO Y DETALLES
class Pedido(models.Model):
    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total_importe = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='TARJETA')
    
    # Simplificamos a un solo responsable para ventas rápidas
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='ventas_realizadas',
        verbose_name="Vendedor/Responsable"
    )

    # Usamos settings.AUTH_USER_MODEL para evitar el error E301
    optico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='pedidos_optico')
    comercial = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='pedidos_comercial')

    def __str__(self):
        return f"Ticket {self.id} - {self.fecha.strftime('%d/%m/%Y')}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    # Guardamos el precio del momento de la venta por si el producto sube de precio mañana
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"