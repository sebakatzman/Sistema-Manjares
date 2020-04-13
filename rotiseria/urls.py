from django.urls import path 
from rotiseria.View.Administrador import CrearProducto, ListarProducto, BorrarProducto,editarProducto, CrearCategoria, ListarCategorias, BorrarCategoría, index, indexAdministrador, editarcategoria, locales 
from rotiseria.View.Recepcionista import CrearBloque, ListarBloque, BorrarBloque, ListarPedido, pedidosConfirmados, confirmar_pedido, rechazar_pedido, pedidosRechazados, pedidosListos, añadir_bloque, enviar_repartidor, nuevo_bloque, pedido_entregado, historial_pedidos 
from rotiseria.View.Cliente import CrearCliente, ListarCliente, BorrarCliente, CrearPedido, indexCliente, quienesSomos, contacto 
from rotiseria.View.Repartidor import ListarDatosMapa, entregar_pedido 
from rotiseria.View.Sesion import SignIn, register, login 
from rotiseria.View.Carrito import VistaCarrito 
from django.contrib.auth.views import logout_then_login

urlpatterns = [
path('indexAdministrador',indexAdministrador, name = 'index_administrador'),
path('locales', locales, name = 'locales'),
path('editarProducto/<int:id_producto>', editarProducto, name = 'editar_producto'),
path('crear_Producto',CrearProducto.as_view(), name = 'crear_producto'),
path('listarProductos',ListarProducto.as_view(), name = 'listar_producto'),
path('borrarProducto/<str:nombrep>/', BorrarProducto, name='borrar_producto'),

path('editarCategoría/<str:nombre>', editarcategoria, name = 'editar_categoria'),
path('crearCategoría',CrearCategoria.as_view(), name = 'crear_categoria'),
path('listarCategorías',ListarCategorias.as_view(), name = 'listar_categoria'),
path('borrarCategoría/<str:nombrec>/', BorrarCategoría, name='borrar_categoria'),

path('crearBloque',CrearBloque.as_view(), name = 'crear_bloque'),
path('listarBloques',ListarBloque.as_view(), name = 'listar_bloque'),
path('borrarBloque/<int:id>/', BorrarBloque, name='borrar_bloque'),

path('crearCliente',CrearCliente.as_view(), name = 'crear_cliente'),
path('listarClientes',ListarCliente.as_view(), name = 'listar_cliente'),
path('borrarCliente/<int:dni>/', BorrarCliente, name='borrar_cliente'),

path('', indexCliente, name='indexCliente'),
path('indexUsuario', index, name = "indexUsuario"),
path('crearPedido',CrearPedido.as_view(), name = 'crear_pedido'),

path('quienesSomos',quienesSomos, name = 'quienesSomos'),
path('contacto',contacto, name = 'contacto'),

# Urls del recepcionista
path('recepcionista',ListarPedido.as_view(), name = 'recepcionista'),
path('pedidosConfirmados', pedidosConfirmados, name = 'pedidos_confirmados'),
path('pedidosRechazados', pedidosRechazados, name = 'pedidos_rechazados'),
path('pedidosListos', pedidosListos, name = 'pedidos_listos'),
path('añadir_bloque/<int:id>/', añadir_bloque, name = 'añadir_bloque'),
path('confirmar_pedido/<int:id>/', confirmar_pedido, name = 'confirmar_pedido'),
path('rechazar_pedido/<int:id>/', rechazar_pedido, name = 'rechazar_pedido'),
path('enviar_repartidor', enviar_repartidor, name = 'enviar_repartidor'),
path('nuevo_bloque', nuevo_bloque, name = 'nuevo_bloque'),
path('pedido_entregado/<int:id>/', pedido_entregado, name='pedido_entregado'),
path('historial_pedidos', historial_pedidos, name='historial_pedidos'),

path('quienesSomos',quienesSomos, name = 'quienesSomos'),

#repartidor
path('repartidor',ListarDatosMapa.as_view(), name = 'listar_datos_mapa'),
path('entregar_pedido/<int:id_pedido>/',entregar_pedido, name = 'entregar_pedido'),

#iniciar sesion
path('accounts/login/',login, name = 'login'),
#cerrar sesion
path('logout/',logout_then_login, name = 'logout'),
path('registro',register, name = 'registro'),

#URLs para operar con el carrito de compras
path('carrito', VistaCarrito.obtenerCarrito, name = "carrito"),
path('agregaritem', VistaCarrito.agregarItem, name = "agregaritem"),
path('eliminarItem', VistaCarrito.eliminarItem, name = "eliminarItem"),
path('confirmarPedido', VistaCarrito.confirmarPedido, name = "confirmarPedido"),
]