from django.views.generic import CreateView, ListView,UpdateView
from django.shortcuts import *
from rotiseria.models import Producto, Categoría
from rotiseria.forms import ProductoForm, CategoriaForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission

def index(request):
    return render(request, 'base.html')

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_admin')
def indexAdministrador(request):
    return render(request, 'Administrador/indexAdministrador.html')

class CrearProducto (CreateView):
    model = Producto
    form_class= ProductoForm   
    template_name = 'Administrador/crearproducto.html'
    success_url = reverse_lazy('index_administrador')
     
    def get(self, request):
        if not(request.user.has_perm('rotiseria.es_admin')):
            return redirect(reverse_lazy('login'))
        categorias = Categoría.objects.all()
        return render(request, 'Administrador/crearproducto.html', {"categorias": categorias})

class ListarProducto (ListView):
    model = Producto
    template_name = "Administrador/listarproducto.html"
    form_class = ProductoForm

    def get(self, request, *args, **kwargs):
        if not(request.user.has_perm('rotiseria.es_admin')):
            return redirect(reverse_lazy('login'))
        productos = Producto.objects.all()
        context_dict = {'productos': productos}
        return render(request, self.template_name, context=context_dict)


@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_admin')
def BorrarProducto(request, nombrep):
    producto = Producto.objects.get(nombre=nombrep)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_producto')
    return render(request, 'Administrador/borrarproducto.html', {'producto':producto})

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_admin')
def editarProducto(request, id_producto):
    producto = Producto.objects.get (id= id_producto)
    categorias = Categoría.objects.all()
    if request.method == 'GET':
        form= ProductoForm(instance=producto)
    else:
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
        return redirect('listar_producto')
    return render (request, 'Administrador/editarProducto.html', {'form':form, 'producto':producto,'categorias':categorias})

class CrearCategoria(CreateView):
    model = Categoría
    form_class = CategoriaForm
    template_name = 'Administrador/crearcategoria.html'
    success_url = reverse_lazy('index_administrador')

    def get(self, request):
        if not(request.user.has_perm('rotiseria.es_admin')):
            return redirect(reverse_lazy('login'))
        categorias = Categoría.objects.all()
        return render(request, self.template_name, {"categorias": categorias})


class ListarCategorias (ListView):
    model = Categoría
    template_name = "Administrador/listarcategorías.html"
    form_class = CategoriaForm

    def get(self, request, *args, **kwargs):
        if not(request.user.has_perm('rotiseria.es_admin')):
            return redirect(reverse_lazy('login'))
        categorías = Categoría.objects.all()
        context_dict = {'categorías': categorías}
        return render(request, self.template_name, context=context_dict)

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_admin')
def BorrarCategoría(request, nombrec):
    categoría = Categoría.objects.get(nombre=nombrec)
    if request.method == 'POST':
        categoría.delete()
        return redirect('listar_categoria')
    return render(request, 'Administrador/borrarcategoría.html', {'categoría':categoría})

@login_required(redirect_field_name='login')
@permission_required('rotiseria.es_admin')
def editarcategoria (request, nombre):
    categoria = Categoría.objects.get(nombre = nombre)
    if request.method == 'GET':
        form = CategoriaForm(instance=categoria)
    else:
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
        return redirect('listar_categoria')
    return render (request, 'Administrador/editarcategoria.html', {'form':form, 'categoria':categoria})        

def locales(request):
    return render(request, 'locales.html')

def locales(request):
    return render(request, 'cliente/locales.html')