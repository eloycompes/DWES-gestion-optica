from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Cita, Consulta, Graduacion, Fabricante, Producto, Pedido

# Personalización del modelo de Usuario para que se vea el Rol en el Admin
class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'nombre', 'apellidos', 'rol', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Rol', {'fields': ('rol', 'nombre', 'apellidos')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Rol', {'fields': ('rol', 'nombre', 'apellidos')}),
    )

admin.site.register(Usuario, CustomUserAdmin)

# Configuración para que la Graduación aparezca dentro de la Consulta (Inline)
class GraduacionInline(admin.StackedInline):
    model = Graduacion
    can_delete = False

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'optico', 'fecha', 'motivo')
    search_fields = ('cliente__nombre', 'cliente__dni')
    inlines = [GraduacionInline] # Esto permite rellenar la graduación al crear la consulta

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellidos', 'telefono')
    search_fields = ('dni', 'nombre', 'apellidos')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'cliente', 'optico', 'estado')
    list_filter = ('estado', 'fecha_hora')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'fabricante', 'precio', 'stock')
    list_filter = ('categoria', 'fabricante')
    search_fields = ('nombre',)

admin.site.register(Fabricante)
admin.site.register(Pedido)