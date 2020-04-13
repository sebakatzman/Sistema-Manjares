from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import json as simplejson
from rotiseria.models import Producto, Bloque, Pedido, EstadoPedido, Cliente, PedidoProducto, Mapa
from rotiseria.forms import PedidoAlimentoForm, ProductoIDForm, ProductoIDForm, DatosClienteForm
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import mercadopago
import json
from datetime import datetime
from datetime import date

mp = mercadopago.MP("2976477610493912", "36kgwdIqyhQeJylWXK8ftz692RzBWIYg")

#Vista del carrito donde se definen varios metodos importantes
class VistaCarrito(View):

    def obtenerCarrito(request):
        if not (request.session['alimentos']):
            messages.warning(request, 'Debe agregar por lo menos 1 producto a su carrito.')
            return HttpResponseRedirect('/')
        else:
            form = ProductoIDForm()
            alimentos = request.session['alimentos']
            lista = []
            total = 0
            #datos[0] -> id alimentoCarta // datos[1] -> cantidad
            for alimentoID, datos  in alimentos.items():
                alimento=get_object_or_404(Producto, id = int(alimentoID))
                subtotal = getattr(alimento, 'precioActual')*datos[1]
                lista.append({'alimentoID': alimento.id,
                            'alimentoNombre': alimento.nombre,
                            'precio': alimento.precioActual,
                            'cantidad': datos[1],
                            'subtotal': subtotal})
                total += subtotal

            preference = {
                "items": [
                    {
                        "title": "Manjares del Beagle",
                        "quantity": 1,
                        "currency_id": "ARS",
                        "unit_price": float(total)
                    }
                ]
            }
            preferenceResult = mp.create_preference(preference)

            return render(request, "Cliente/carrito.html", {
                'form'  : form,
                'lista' : lista,
                'total' : total,
                'preference_id' : preferenceResult['response']['id'],
            }) 

    @csrf_protect
    def agregarItem(request):
     
        if request.method == 'POST':
            form = PedidoAlimentoForm(request.POST)
            if form.is_valid():
                contenido = {
                    'alimentoID' : form.cleaned_data['alimento'],
                    'cantidad' : form.cleaned_data['cantidad']
                }
            request.session['items'] = request.session['items'] + contenido['cantidad']
            lista = request.session['alimentos']
            elemento = str(contenido['alimentoID'])
            cantidad = contenido
            if  elemento in request.session['alimentos']:
                    print ('si esta')
                    cant = lista[elemento][1]
                    request.session['alimentos'][elemento][1] = contenido['cantidad'] + cant
            else:
                    print ('no esta')
                    request.session['alimentos'][contenido['alimentoID']] = [contenido['alimentoID'], contenido['cantidad']]
                    print (request.session['alimentos'])
        return HttpResponse("ok")

    def eliminarItem(request):

        if request.method == 'POST':
            form = ProductoIDForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data['alimento']
                request.session['items'] = request.session['items'] - request.session['alimentos'][str(id)][1]
                request.session['alimentos'].pop(str(id),None)
                return HttpResponseRedirect('/carrito')

    @csrf_protect
    def confirmarPedido(request):

        if request.method == 'POST':
            form = DatosClienteForm(request.POST)
            diaHoy = datetime.now()
            horaRoti = datetime(2019, 12, 12, 14, 59, 59, 00000)
            if (format(diaHoy.hour) < format(horaRoti.hour)):
                if form.is_valid():    
                    nombreApellido = form.cleaned_data['nombreApellido']
                    celular = form.cleaned_data['celular']
                    descripcion = form.cleaned_data['descripcion']
                    dire = form.cleaned_data['direccion']
                    latitud = form.cleaned_data['latitud']
                    longitud = form.cleaned_data['longitud']
                    pago = form.cleaned_data['pago']
                    #Obtenemos solo la direccion con el numero, nada mas...
                    direccion = VistaCarrito.obtenerDireccion(dire)
                    estaEnbd = False
                    if direccion == '': #Si la direccion es vacia es xq retira en la rotiseria
                        direccionCliente = Mapa.objects.get(direccion = 'General Manuel Belgrano 43')
                    else:
                        #Si la direccion esta cargada en el modelo mapa, lo traemos y hacemos la relacion de pedido con mapa 
                        direcciones = Mapa.objects.all()
                        for d in direcciones:
                            if d.direccion == direccion:
                                direccionCliente = d
                                estaEnbd = True
                        if estaEnbd == False:
                            direccionCliente = Mapa.objects.create(latitud = latitud, longitud = longitud, direccion = direccion)
                            direccionCliente.save()
                    alimentos = request.session['alimentos']
                    bloque = Bloque.objects.get(id = 1)
                    estadoPedido = EstadoPedido.objects.get(estado = 'pendiente')
                    pedido = Pedido.objects.create(bloque = bloque, nombre_cliente = nombreApellido, estadoPedido = estadoPedido, descripcion = descripcion, telefono_cliente = celular, mapa = direccionCliente)
                    total = 0
                    #datos[0] -> id alimento // datos[1] -> cantidad de alimentos
                    for alimentoID, datos  in alimentos.items():
                        producto = Producto.objects.get(id = int(alimentoID))
                        subtotal = getattr(producto, 'precioActual')*datos[1]
                        total += subtotal
                        precioActual = producto.precioActual
                        pedidoProducto = PedidoProducto.objects.create(producto=producto, pedido=pedido,
                                                                    precioVariable= precioActual, subtotal=subtotal,
                                                                    cantidad=datos[1])
                    pedido.pago = pago
                    pedido.total = total
                    pedido.save()
                    request.session.flush()
                    messages.warning(request, 'Gracias por realizar tu pedido.')
                    return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Formulario inválido. Completar todos los datos.')
                    return HttpResponseRedirect('/carrito')
            else: 
                messages.warning(request, 'Lo sentimos, debe pedir dentro del horario de la rotiseria.')
                return HttpResponseRedirect('/carrito')
            

    def obtenerDireccion(dire):
        i = 0
        d = ''
        if dire != '-':
            while dire[i] != ',':
                d = d + dire[i]
                i = i + 1
        return d

    def obtenerDescripcion(desc):
        if desc == '-':
            desc = ""
        return desc
