from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from rotiseria.models import Pedido, Mapa, Bloque, EstadoPedido
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_repart')
def mapa(request):
    return render (request,'Repartidor/index.html')

class ListarDatosMapa (ListView):
    model = Mapa
    template_name = "Repartidor/index.html"

    def get(self, request, *args, **kwargs):
        if not(request.user.has_perm('rotiseria.es_repart')):
            return redirect(reverse_lazy('login'))
        bloques = Bloque.objects.all()
        #bloques empiezan del ID 0 (cero)
        id = len(bloques) - 1
        ultimo_Bloque = bloques[id]

        #pedidos_bloque = Pedido.objects.filter(bloque = ultimo_Bloque.id, estadoPedido = "enviado")
        #se filtran los pedidos en estado listo, ya que el repartidor al presionar el boton entregado
        #cambia el estado del pedido a "estregado".
        estadoEnviado = EstadoPedido.objects.get(estado = 'enviado')
        pedidos_bloque = Pedido.objects.filter(bloque = ultimo_Bloque.id, estadoPedido = estadoEnviado).order_by('-id')
        context_dict = {'pedidos_bloque': pedidos_bloque}
        return render(request, self.template_name, context=context_dict)

def entregar_pedido(request, id_pedido):
    bloques = Bloque.objects.all()
    #bloques empiezan del ID 0 (cero)
    id_bloque = len(bloques) - 1
    ultimo_Bloque = bloques[id_bloque]
    pedidos_bloque = Pedido.objects.filter(bloque = ultimo_Bloque.id).order_by('-id')
    estadoEntregado = EstadoPedido.objects.get(estado = 'entregado')
    for pedido in pedidos_bloque:
        #si el id de todos los pedidos es igual al pedido a marcar como entregado, entonces...
        if pedido.id == id_pedido:
            #se cambia el estado anterior
            pedido.estadoPedido = estadoEntregado
            pedido.save()

    return HttpResponseRedirect('/repartidor')