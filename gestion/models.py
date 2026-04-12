from django.db import models
from django.contrib.auth.models import AbstractUser

# Generalización de Usuario
class Usuario(AbstractUser):
    ROLES = [
        ('ADMIN', 'Admin'),
        ('DIRECTOR', 'Director'),
        ('OPTICO', 'Óptico'),
        ('COMERCIAL', 'Comercial'),
        ('CLIENTE', 'Cliente'),
    ]
    rol = models.CharField(max_length=15, choices=ROLES, default='COMERCIAL')
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} - {self.rol}"

# Clase Cliente
class Cliente(models.Model):
    dni = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# Clase Fabricante
class Fabricante(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Clase Producto
class Producto(models.Model):
    CAT_CHOICES = [('MONTURA', 'Montura'), ('LENTE', 'Lente'), ('OTROS', 'Otros')]
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CAT_CHOICES)
    subcategoria = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Clase Cita
class Cita(models.Model):
    ESTADOS = [('PENDIENTE', 'Pendiente'), ('FINALIZADA', 'Finalizada'), ('CANCELADA', 'Cancelada')]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    optico = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'OPTICO'})
    fecha_hora = models.DateTimeField()
    motivo_cita = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

# Clase Consulta (Anamnesis)
class Consulta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    optico = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'OPTICO'})
    fecha = models.DateField(auto_now_add=True)
    motivo = models.TextField()
    ant_medicos = models.TextField(blank=True)
    ant_oculares = models.TextField(blank=True)
    pantallas = models.CharField(max_length=100)
    gafas_sol = models.BooleanField(default=False)
    lentillas = models.BooleanField(default=False)
    recomendaciones = models.TextField(blank=True)

# Clase Graduacion (Composición 1:1 con Consulta)
class Graduacion(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, primary_key=True)
    od_esfera = models.DecimalField(max_digits=5, decimal_places=2)
    od_cilindro = models.DecimalField(max_digits=5, decimal_places=2)
    od_eje = models.IntegerField()
    od_adicion = models.DecimalField(max_digits=5, decimal_places=2)
    od_agudeza = models.DecimalField(max_digits=5, decimal_places=2)
    oi_esfera = models.DecimalField(max_digits=5, decimal_places=2)
    oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2)
    oi_eje = models.IntegerField()
    oi_adicion = models.DecimalField(max_digits=5, decimal_places=2)
    oi_agudeza = models.DecimalField(max_digits=5, decimal_places=2)
    queratometria = models.TextField()
    biomicroscopio = models.TextField()
    tanometria = models.TextField()

# Clase Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    optico = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos_optico', limit_choices_to={'rol': 'OPTICO'})
    comercial = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos_comercial', limit_choices_to={'rol': 'COMERCIAL'})
    fecha = models.DateTimeField(auto_now_add=True)
    total_importe = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    productos = models.ManyToManyField(Producto)