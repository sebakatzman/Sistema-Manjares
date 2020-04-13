from django.views.generic import CreateView, ListView
from rotiseria.models import Bloque, Pedido, PedidoProducto, EstadoPedido, Mapa
from rotiseria.forms import BloqueForm, PedidoForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin

class CrearBloque(CreateView):
    model = Bloque
    form_class = BloqueForm
    template_name = 'Recepcionista/crearBloque.html'
    success_url = reverse_lazy('index')

    def get (self,request):
        if not(request.user.has_perm('rotiseria.es_recep')): 
            return redirect(reverse_lazy('login'))   

class ListarBloque(ListView):
    model = Bloque
    template_name = "Recepcionista/listarBloque.html"
    form_class = BloqueForm

    def get(self, request, *args, **kwargs):
        if not(request.user.has_perm('rotiseria.es_repart')):
                return redirect(reverse_lazy('login'))
        bloques = Bloque.objects.all()
        context_dict = {'bloques': bloques}
        return render(request, self.template_name, context=context_dict)

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def BorrarBloque(request, id):
	bloque = Bloque.objects.get(id=id)
	if request.method == 'POST':
		bloque.delete()
		return redirect('index')
	return render(request, 'Recepcionista/borrarBloque.html', {'bloque':bloque})

class ListarPedido(ListView):
    model = Pedido
    template_name = "Recepcionista/listarPedidos.html"
    form_class = PedidoForm

    def get(self, request, *args, **kwargs):
        if not(request.user.has_perm('rotiseria.es_recep')):
                return redirect(reverse_lazy('login'))
        #Con esto le paso el total como unico valor sumado de todos los productos del pedido
        pedidos = Pedido.objects.order_by('-id')
        pedidoProductos = PedidoProducto.objects.all()
        context_dict = {'pedidos': pedidos, 'pedidoProductos': pedidoProductos}
        return render(request, self.template_name, context=context_dict)

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def pedidosConfirmados(request):
    pedidos = Pedido.objects.order_by('-id')
    pedidoProductos = PedidoProducto.objects.all()
    context_dict = {'pedidos': pedidos, 'pedidoProductos': pedidoProductos}
    return render(request, 'Recepcionista/listarPedidosConfirmados.html', context=context_dict)

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def confirmar_pedido(request, id):
    pedido = Pedido.objects.get(id =id)
    estadoConfirmado = EstadoPedido.objects.get(estado = 'confirmado')
    pedido.estadoPedido = estadoConfirmado
    pedido.save()
    return HttpResponseRedirect('/recepcionista')

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def rechazar_pedido(request, id):
    pedido = Pedido.objects.get(id = id)
    estadoDelPedido = EstadoPedido.objects.get(estado = 'rechazado')
    pedido.estadoPedido = estadoDelPedido
    pedido.save()
    return HttpResponseRedirect('/recepcionista')

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def pedidosRechazados(request):
    pedidos = Pedido.objects.order_by('-id')
    pedidoProductos = PedidoProducto.objects.all()
    context_dict = {'pedidos': pedidos, 'pedidoProductos': pedidoProductos}
    return render(request, 'Recepcionista/listarPedidosRechazados.html', context=context_dict)    

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def pedidosListos(request):
    pedidos = Pedido.objects.order_by('-id')
    pedidoProductos = PedidoProducto.objects.all()
    context_dict = {'pedidos': pedidos, 'pedidoProductos': pedidoProductos}
    return render(request, 'Recepcionista/listarPedidosListos.html', context=context_dict)  

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def añadir_bloque(request, id):
    pedido = Pedido.objects.get(id = id)
    #me ubico en el ultimo bloque
    bloques = Bloque.objects.all()
    #tengo la longitud del bloque
    id_bloque = len(bloques) - 1
    ultimo_Bloque = bloques[id_bloque]
    
    pedido.bloque = ultimo_Bloque
    estadoEnviado = EstadoPedido.objects.get(estado = 'listo')
    pedido.estadoPedido = estadoEnviado
    pedido.save()
    return HttpResponseRedirect('/pedidosConfirmados')

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def enviar_repartidor(request):
    pedidos = Pedido.objects.all()
    estadoEnviado = EstadoPedido.objects.get(estado = 'enviado')
    for pedido in pedidos:
        if pedido.estadoPedido.estado == 'listo':
            #si el pedido esta listo, se lo cambia a enviado
            pedido.estadoPedido = estadoEnviado
            pedido.save()
    return HttpResponseRedirect('/pedidosListos')

#se crea un nuevo bloque
@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def nuevo_bloque(request):
    ultimo_bloque = Bloque.objects.create()
    estadoPedido = EstadoPedido.objects.get(estado = 'enviado')
    #PREGUNTAR SI LA DIRECCION YA EXISTE, SINO CREARLA (XQ SE CREAN MUCHAS IGUALES)
    direccionCliente = Mapa.objects.get(direccion = "General Manuel Belgrano 43")
    #AGREGAR EN DESCRIPCION - "INICIO" O EN PAGO - "SIN PAGAR"
    pedido = Pedido.objects.create(bloque = ultimo_bloque, nombre_cliente = "Manjares del Beagle", estadoPedido = estadoPedido, descripcion = "INICIO", telefono_cliente = 425067, mapa = direccionCliente, pago = "-")

    pedidos = Pedido.objects.all()
    context_dict = {'ultimo_bloque': ultimo_bloque, 'pedidos': pedidos}
    return render(request, 'Recepcionista/listarPedidosConfirmados.html', context=context_dict)  

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def pedido_entregado(request, id):
    pedido = Pedido.objects.get(id = id)
    estadoDelPedido = EstadoPedido.objects.get(estado = 'entregado')
    pedido.estadoPedido = estadoDelPedido
    pedido.save()
    return HttpResponseRedirect('/pedidosConfirmados')

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_recep')
def historial_pedidos(request):
    pedidos = Pedido.objects.order_by('-id')
    pedidoProductos = PedidoProducto.objects.all()
    context_dict = {'pedidos': pedidos, 'pedidoProductos': pedidoProductos}
    return render(request, 'Recepcionista/historialPedidos.html', context=context_dict) 