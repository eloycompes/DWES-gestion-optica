from django import forms
from .models import Cita, Cliente, Encargo, Graduacion, Pedido, Consulta, Producto, Usuario


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni', 'nombre', 'apellidos', 'telefono', 'fecha_nacimiento', 'email']
        widgets = {
            # El secreto está en format='%Y-%m-%d'
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Esto asegura que el valor cargado también tenga el formato correcto
        if self.instance and self.instance.fecha_nacimiento:
            self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')

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


from django import forms
from .models import Encargo, Producto, Graduacion, Usuario

class EncargoForm(forms.ModelForm):
    # Campo extra para el buscador
    montura = forms.ModelChoiceField(
        queryset=Producto.objects.filter(categoria__nombre="Monturas"),
        required=False,
        label="Buscar Montura (Código o Nombre)",
        widget=forms.Select(attrs={'class': 'form-control buscador-monturas'})
    )

    def __init__(self, *args, **kwargs):
        # Extraemos el cliente antes de llamar al super
        cliente = kwargs.pop('cliente', None)
        super().__init__(*args, **kwargs)
        
        # A. Si estamos EDITANDO: Pre-cargamos el buscador con la montura guardada
        if self.instance and self.instance.pk:
            prod = Producto.objects.filter(nombre=self.instance.montura_marca_modelo).first()
            if prod:
                self.fields['montura'].initial = prod

        # B. Filtrar graduaciones solo del cliente actual
        if cliente:
            self.fields['graduacion'].queryset = Graduacion.objects.filter(
                consulta__cliente=cliente
            ).order_by('-consulta__fecha')
        
        # C. Cargar lista de vendedores
        self.fields['vendedor'].queryset = Usuario.objects.all()
        self.fields['vendedor'].empty_label = "Seleccione un vendedor"

    def clean(self):
        cleaned_data = super().clean()
        montura_seleccionada = cleaned_data.get('montura')
        
        # D. Si se eligió una montura del buscador, la pasamos al campo de texto del modelo
        if montura_seleccionada:
            cleaned_data['montura_marca_modelo'] = montura_seleccionada.nombre
            # Si el precio está vacío, ponemos el del producto
            if not cleaned_data.get('montura_precio'):
                cleaned_data['montura_precio'] = montura_seleccionada.precio
                
        return cleaned_data

    class Meta:
        model = Encargo
        exclude = ['cliente', 'fecha_encargo', 'estado', 'total_encargo']
        widgets = {
            'montura_marca_modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca, modelo...'}),
            'montura_en_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'montura_precio': forms.NumberInput(attrs={'class': 'form-control precio-input', 'step': '0.01'}),
            'pagado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'proveedor_lentes': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-select'}),
            'od_tipo': forms.Select(attrs={'class': 'form-select'}),
            'od_indice': forms.Select(attrs={'class': 'form-select'}),
            'od_codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'od_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'od_precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'oi_tipo': forms.Select(attrs={'class': 'form-select'}),
            'oi_indice': forms.Select(attrs={'class': 'form-select'}),
            'oi_codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'oi_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'oi_precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vendedor': forms.Select(attrs={'class': 'form-select'}),
            'graduacion': forms.Select(attrs={'class': 'form-select'}),
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['cliente', 'optico', 'fecha_hora', 'motivo_cita', 'estado']
        widgets = {
            # 'datetime-local' permite elegir día y hora en un solo selector
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'optico': forms.Select(attrs={'class': 'form-select'}),
            'motivo_cita': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Revisión anual'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si venimos desde la ficha de un cliente, podemos querer pre-seleccionarlo
        if 'initial' in kwargs and 'cliente' in kwargs['initial']:
            self.fields['cliente'].disabled = True