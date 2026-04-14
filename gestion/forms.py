from django import forms
from .models import Encargo, Graduacion, Pedido, Consulta, Producto, Usuario


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


class EncargoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente', None)
        super().__init__(*args, **kwargs)
        
        if cliente:
            self.fields['graduacion'].queryset = Graduacion.objects.filter(
                consulta__cliente=cliente
            ).order_by('-consulta__fecha')
        
        # CAMBIO AQUÍ: Usamos tu modelo Usuario
        self.fields['vendedor'].queryset = Usuario.objects.all()
        self.fields['vendedor'].empty_label = "Seleccione un vendedor"

    class Meta:
        model = Encargo
        exclude = ['cliente', 'fecha_encargo', 'estado']
        
        widgets = {
            # Montura
            'montura_marca_modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca, modelo, calibre...'}),
            'montura_en_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Común Cristales
            'proveedor_lentes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Essilor, Hoya...'}),
            'material': forms.Select(attrs={'class': 'form-select', 'id': 'id_material'}),
            
            # Ojo Derecho (OD)
            'od_tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_od_tipo'}),
            'od_indice': forms.Select(attrs={'class': 'form-select', 'id': 'id_od_indice'}), # Widget de Select para los índices
            'od_codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código interno'}),
            'od_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre comercial lente'}),
            'od_precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

            # Ojo Izquierdo (OI)
            'oi_tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_oi_tipo'}),
            'oi_indice': forms.Select(attrs={'class': 'form-select', 'id': 'id_oi_indice'}), # Widget de Select para los índices
            'oi_codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código interno'}),
            'oi_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre comercial lente'}),
            'oi_precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

            'vendedor': forms.Select(attrs={'class': 'form-select'}),
            'graduacion': forms.Select(attrs={'class': 'form-select'}),
        }