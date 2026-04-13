from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
    # Pruebas de Gabinete
    queratometria = models.CharField(max_length=255, blank=True)
    biomicroscopio = models.TextField(blank=True) # Uso TextField por si el óptico necesita explayarse
    tanometria = models.CharField(max_length=255, blank=True) # Mantengo tu nombre "tanometria"

    def __str__(self):
        return f"Graduación técnica - {self.consulta.cliente.nombre}"

# 6. FABRICANTE
class Fabricante(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# 7. PRODUCTO
class Producto(models.Model):
    CATEGORIAS = (
        ('Montura', 'Montura'),
        ('Lente', 'Lente'),
        ('Accesorio', 'Accesorio'),
        ('Contactología', 'Contactología'),
    )
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    subcategoria = models.CharField(max_length=50, help_text="Ej: Monofocal, Hidrogel, Pasta...")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.fabricante.nombre} ({self.categoria})"

# 8. PEDIDO
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    optico = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pedidos_validados', limit_choices_to={'rol': 'Optico'})
    comercial = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pedidos_vendidos', limit_choices_to={'rol': 'Comercial'})
    fecha = models.DateField(auto_now_add=True)
    total_importe = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    productos = models.ManyToManyField(Producto)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"