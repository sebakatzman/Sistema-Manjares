from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect
from rotiseria.models import Cliente, Pedido, Producto, Categoría, PedidoProducto
from rotiseria.forms import ClienteForm, PedidoForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def contacto(request):
    request.session.flush()
    categorias = Categoría.objects.all()
    contexto = {'categorias': categorias}
    return render(request, 'Cliente/contacto.html', contexto)

def quienesSomos(request):
    request.session.flush()
    categorias = Categoría.objects.all()
    contexto = {'categorias': categorias}
    return render(request, 'Cliente/quienesSomos.html', contexto)

def indexCliente(request):
    if 'alimentos'not in request.session:
        request.session['alimentos'] = {}
        request.session['items'] = 0
            
    categorias = Categoría.objects.all()
    productos = Producto.objects.all()
    #Numero de visitas contadas en esta variable de sesion
    num_visitas = request.session.get('num_visitas', 0)
    request.session['num_visitas'] = num_visitas+1
    items = request.session['items']
    print (items)
    contexto = {'productos': productos, 'categorias': categorias, 'num_visitas': num_visitas, 'items': items}
    return render(request, 'Cliente/index.html', contexto)

class CrearCliente(CreateView):
    login_required(login_url='registro')
    model = Cliente
    form_class = ClienteForm
    template_name = 'Cliente/crearCliente.html'
    success_url = reverse_lazy('index')

@method_decorator(login_required, name='dispatch')
class ListarCliente(ListView):
    login_required(login_url='registro')
    model = Cliente
    template_name = "Cliente/listarCliente.html"
    form_class = ClienteForm

    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all()
        context_dict = {'clientes': clientes}
        return render(request, self.template_name, context=context_dict)

@login_required(redirect_field_name='login')
def BorrarCliente(request, dni):
	cliente = Cliente.objects.get(dni=dni)
	if request.method == 'POST':
		cliente.delete()
		return redirect('index')
	return render(request, 'Cliente/borrarCliente.html', {'cliente':cliente})

class CrearPedido(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Cliente/crearPedido.html'
    success_url = reverse_lazy('index')


