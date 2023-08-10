from django import forms
from django.forms import formset_factory
from .models import Clientes , Productos , Venta , VentaItem ,Pago


class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre','telefono']
class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre','descripcion','precio','cantidad']

class VentaItemForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Productos.objects.all(), label='Producto')
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')

VentaItemFormSet = formset_factory(VentaItemForm, extra=1)

# VentaForm using formsets
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'forma_pago']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the formset using the VentaItemForm
        self.formset = VentaItemFormSet(*args, **kwargs)

    def is_valid(self):
        # Validate both the main form and the formset
        return super().is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        # Save the main form instance
        venta = super().save(commit=commit)

        # Save the related VentaItemForm instances
        if commit:
            total_venta = 0  # Variable to store the total price of the entire venta
            for form in self.formset:
                producto = form.cleaned_data['producto']
                cantidad = form.cleaned_data['cantidad']

                # Calculate the total price for this VentaItem based on quantity and product price
                total_item = producto.precio * cantidad
                total_venta += total_item  # Add the item's total to the venta's total

                # Create the VentaItem instance
                item = VentaItem.objects.create(venta=venta, producto=producto, cantidad=cantidad)

            # Update the total price for the entire venta
            venta.total_precio = total_venta
            venta.save()

        return venta

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['cliente','producto', 'fecha', 'metodo_pago','ventas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }