from django.contrib import admin

from .models.bloque import Bloque
from .models.categoría import Categoría
from .models.cliente import Cliente
from .models.estadopedido import EstadoPedido
from .models.pedido import Pedido
from .models.pedidoproducto import PedidoProducto
from .models.producto import Producto
from .models.rol import Rol
from .models.usuario import Usuario
from .models.mapa import Mapa

admin.site.register(Bloque)
admin.site.register(Categoría)
admin.site.register(Cliente)
admin.site.register(EstadoPedido)
admin.site.register(Pedido)
admin.site.register(PedidoProducto)
admin.site.register(Producto)
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Mapa)