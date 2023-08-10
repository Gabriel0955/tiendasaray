# Generated by Django 4.2.4 on 2023-08-10 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0002_detallefactura_factura_detallefactura_factura_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('metodo_pago', models.CharField(max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.clientes')),
                ('producto', models.ManyToManyField(related_name='productos', to='Inventario.productos')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('forma_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta_credito', 'Tarjeta de Crédito'), ('tarjeta_debito', 'Tarjeta de Débito'), ('transferencia', 'Transferencia Bancaria'), ('paypal', 'PayPal'), ('cheque', 'Cheque'), ('pago_movil', 'Pago Móvil'), ('criptomonedas', 'Criptomonedas'), ('pago_contra_entrega', 'Pago contra Entrega'), ('pago_a_plazos', 'Pago a Plazos')], max_length=50, null=True)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('total_precio', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('estado', models.IntegerField(default=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.clientes')),
                ('producto', models.ManyToManyField(related_name='Producto', to='Inventario.productos')),
            ],
        ),
        migrations.CreateModel(
            name='VentaItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_uni', models.FloatField(default=0)),
                ('subtotal', models.FloatField(default=0)),
                ('estado', models.IntegerField(default=1)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.productos')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Inventario.venta')),
            ],
        ),
        migrations.DeleteModel(
            name='Empleados',
        ),
        migrations.AddField(
            model_name='pago',
            name='ventas',
            field=models.ManyToManyField(to='Inventario.venta'),
        ),
    ]
