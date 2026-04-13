from django.contrib import admin
from django.urls import path, include  # Importante añadir 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', include('gestion.urls')), 
]