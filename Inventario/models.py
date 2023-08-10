from django.db import models

class Clientes(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre
class Factura(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Productos, through='DetalleFactura')

    def __str__(self):
        return f'Factura {self.id} - {self.cliente.nombre}'

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle de Factura {self.factura.id} - Producto: {self.producto.nombre}'
class Venta(models.Model):
    cliente = models.ForeignKey('Clientes', on_delete=models.CASCADE)
    producto = models.ManyToManyField('Productos',related_name='Producto')
    fecha = models.DateTimeField(auto_now_add=True)
    FORMAS_DE_PAGO = (
        ('efectivo', 'Efectivo'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('paypal', 'PayPal'),
        ('cheque', 'Cheque'),
        ('pago_movil', 'Pago Móvil'),
        ('criptomonedas', 'Criptomonedas'),
        ('pago_contra_entrega', 'Pago contra Entrega'),
        ('pago_a_plazos', 'Pago a Plazos'),
    )

    forma_pago = models.CharField(max_length=50, choices=FORMAS_DE_PAGO, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    total_precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True ,blank=True, null=True )
    fecha_modificacion = models.DateTimeField(auto_now=True)

    # Otros campos adicionales relevantes para la venta

    def calcular_total(self):
        total = 0
        for item in self.items.all():
            total += item.precio
        return total

    def calcular_subtotal(self):
        subtotales = []
        for item in self.items.all():
            subtotal = item.producto.precio * item.cantidad
            subtotales.append(subtotal)

        return subtotales

class Pago(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    producto = models.ManyToManyField('Productos',related_name='productos')
    ventas = models.ManyToManyField(Venta)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=50)
    # Otros campos relacionados con el pago

    def __str__(self):
        return f"{self.cliente} - {self.fecha}"


class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_uni = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    estado = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.producto} - Cantidad: {self.cantidad}"
    @property
    def precio(self):
        return self.producto.precio * self.cantidad

