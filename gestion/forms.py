from django import forms
from .models import Graduacion, Pedido, Consulta, Producto

class GraduacionForm(forms.ModelForm):
    # Campos virtuales que veremos en el HTML
    od_q1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '7.75'}))
    od_q2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '7.60'}))
    oi_q1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '7.80'}))
    oi_q2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '7.75'}))

    class Meta:
        model = Graduacion
        # IMPORTANTE: Excluimos los originales para gestionarlos nosotros en la vista
        exclude = ['consulta', 'od_queratometria', 'oi_queratometria']
        
        widgets = {
            # Ojo Derecho
            'od_esfera': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'od_cilindro': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'od_eje': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '180'}),
            'od_adicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'od_agudeza': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'od_tonometria': forms.NumberInput(attrs={'placeholder': 'OD', 'class': 'form-control'}),
            
            # Ojo Izquierdo
            'oi_esfera': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'oi_cilindro': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'oi_eje': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '180'}),
            'oi_adicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'oi_agudeza': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),          
            'oi_tonometria': forms.NumberInput(attrs={'placeholder': 'OI', 'class': 'form-control'}),

            'biomicroscopio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


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



class VentaRapidaForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'metodo_pago', 'vendedor']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'vendedor': forms.Select(attrs={'class': 'form-select'}),
        }