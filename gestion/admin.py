from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Fabricante, Producto, Cita, Consulta, Graduacion, Pedido

# Registro del Usuario personalizado
@admin.register(Usuario)
class UsuarioPersonalizadoAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Rol', {'fields': ('rol',)}),
    )
    list_display = ('username', 'email', 'nombre', 'apellidos', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser')

# Registro de Clientes
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellidos', 'telefono')
    search_fields = ('dni', 'nombre', 'apellidos')

# Registro de Productos y Fabricantes
admin.site.register(Fabricante)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'fabricante')
    list_filter = ('categoria', 'fabricante')
    search_fields = ('nombre',)

# Registro de Citas
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'optico', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora')

# Registro de Consulta y Graduación (pueden ir juntos)
admin.site.register(Consulta)
admin.site.register(Graduacion)

# Registro de Pedidos
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'total_importe', 'metodo_pago')
    filter_horizontal = ('productos',)  # Facilita la selección múltiple de productos