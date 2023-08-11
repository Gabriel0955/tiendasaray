from django.shortcuts import render , redirect , get_object_or_404
from .models import Clientes , Productos ,Venta,VentaItem ,Pago
from .forms import ClientesForm , ProductosForm ,VentaForm, VentaItemFormSet,VentaItemForm ,PagoForm

from django.views.generic import ListView , CreateView , UpdateView , DeleteView , View
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from reportlab.lib.units import inch

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Image, Table, TableStyle

def Crear_usuario(request):
    if request.method == 'POST':
        form = ClientesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultar_usuario')
    else:
        form = ClientesForm()
    return render(request,'clientes/crear_cliente.html',{'form':form})

def consultar_usuario(request):
    cliente = Clientes.objects.all()
    return render(request,'clientes/consultar_cliente.html',{'cliente':cliente})

def eliminar_usuario(request, cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)
    cliente.delete()
    return redirect('consultar_usuario')


class ClienteUpdateView(UpdateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'clientes/modificar_cliente.html'
    success_url = reverse_lazy('consultar_usuario')



def crear_producto(request):
    if request.method == 'POST':
        form = ProductosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultar_producto')
    else:
        form = ProductosForm()
    return render(request,'productos/crear_producto.html',{'form':form})

def consultar_producto(request):
    producto = Productos.objects.all()
    return render(request,'productos/consultar_producto.html',{'producto':producto})
def eliminar_producto(request, producto_id):
    empleado = get_object_or_404(Productos, id=producto_id)
    empleado.delete()
    return redirect('consultar_producto')


class ProductoUpdateView(UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/modificar_producto.html'
    success_url = reverse_lazy('consultar_producto')

def consultar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    producto = venta.producto.all()
    context = {
        'venta': venta,
        'producto': producto,
    }

    return render(request, 'ventas/consultar_venta.html', context)


def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=True)

            # Save the related VentaItemForm instances from the formset
            for formset_form in form.formset:
                producto = formset_form.cleaned_data.get('producto')
                cantidad = formset_form.cleaned_data.get('cantidad')
                if producto and cantidad:
                    existing_item = VentaItem.objects.filter(venta=venta, producto=producto).first()
                    if existing_item:
                        existing_item.cantidad = cantidad
                        existing_item.save()
                    else:
                        VentaItem.objects.create(venta=venta, producto=producto, cantidad=cantidad)

            return redirect('consultar_venta', venta_id=venta.id)
    else:
        form = VentaForm()
        form.formset = VentaItemFormSet()

    return render(request, 'ventas/crear_venta.html', {'form': form})



def mostrar_pagos(request):

    pagos = Pago.objects.all()
    productos = Productos.objects.all()
    clientes = Clientes.objects.all()
    venta = Venta.objects.all()

    context = {
        'pagos': pagos,
        'productos': productos,
        'clientes': clientes,
        'venta': venta,
    }

    return render(request, 'pago/consultar_pago.html', context)


def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultar_pago')
    else:
        form = PagoForm()
    producto = Productos.objects.all()
    cliente = Clientes.objects.all()


    context = {
        'form': form,
        'producto': producto,
        'cliente': cliente,

    }
    return render(request, 'pago/agregar_pago.html', context)


def eliminar_pago(request, venta_id):
    pago = get_object_or_404(Venta, id=venta_id)
    pago.delete()
    return redirect('consultar_pago')



def consultar_venta_pdf(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)  # Asegúrate de importar el modelo "Venta" correctamente

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="venta_{venta_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    elements = []

    # Add factura information to the PDF
    elements.append(Paragraph('NOVEDADES & VARIEDADES SARAY', styles['h1']))
    elements.append(Paragraph(f'Vendedora: Meybi Yulexy Aguirre Leiton ', styles['Normal']))

    elements.append(Paragraph('Dirección de la empresa: NUEVE DE OCTUBRE', styles['Normal']))
    elements.append(Paragraph('Ciudad, Código Postal: GUAYAQUIL,090150', styles['Normal']))
    elements.append(Paragraph('Teléfono:0982054389', styles['Normal']))
    elements.append(Spacer(1, 12))  # Add some space between sections
    # Buyer information
    elements.append(Paragraph('Datos del Comprador:', styles['Heading1']))
    elements.append(Paragraph(f'Nombre del cliente: {venta.cliente}', styles['Normal']))
    elements.append(Paragraph(f'Ciudad: Guayaquil', styles['Normal']))
    elements.append(Paragraph(f'Telefono: {venta.cliente.telefono}', styles['Normal']))
    elements.append(Spacer(1, 12))  # Add some space between sections

    # Invoice details
    elements.append(Paragraph('Detalles de la Factura:', styles['Heading1']))
    elements.append(Paragraph(f'Número de Factura: {venta.id}', styles['Normal']))
    elements.append(Paragraph(f'Metodo de pago: {venta.forma_pago}', styles['Normal']))
    elements.append(Paragraph(f'Fecha de emisión: {venta.fecha.strftime("%d/%m/%Y")}', styles['Normal']))
    elements.append(Spacer(1, 12))  # Add some space between sections

    # Table with product information
    data = [['Id','Descripcion','Producto', 'Cantidad', 'Precio Unitario', 'Subtotal']]
    total = 0
    for item in venta.items.all():
        subtotal = item.producto.precio * item.cantidad
        total += subtotal
        data.append([item.producto.id,item.producto.descripcion,item.producto.nombre, item.cantidad, f'${item.producto.precio:.2f}', f'${subtotal:.2f}'])
    data.append(['', '','','', 'Total:', f'${total:.2f}'])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    return response