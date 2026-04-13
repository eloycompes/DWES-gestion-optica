from django import forms
from .models import Graduacion

class GraduacionForm(forms.ModelForm):
    class Meta:
        model = Graduacion
        # Excluimos 'consulta' porque la asignaremos automáticamente en la vista
        exclude = ['consulta']
        
        widgets = {
            # Ojo Derecho
            'od_esfera': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'od_cilindro': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'od_eje': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '180'}),
            'od_adicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'od_agudeza': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            
            # Ojo Izquierdo
            'oi_esfera': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'oi_cilindro': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'oi_eje': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '180'}),
            'oi_adicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'oi_agudeza': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            
            # Gabinete
            'queratometria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 7.75 / 7.80'}),
            'biomicroscopio': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'tanometria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 15 mmHg'}),
        }

from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta

        fields = [
            'motivo', 'ant_medicos', 'ant_oculares', 
            'pantallas', 'gafas_sol', 'lentillas', 'recomendaciones'
        ]
        widgets = {
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'ant_medicos': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'ant_oculares': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'pantallas': forms.TextInput(attrs={'class': 'form-control'}),
            'gafas_sol': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lentillas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recomendaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
        }