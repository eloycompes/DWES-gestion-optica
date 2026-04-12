from django.contrib import admin
from django.urls import path
from gestion import views # Importamos las vistas de tu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]