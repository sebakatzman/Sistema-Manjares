from django.db import models
from rotiseria.models.producto import Producto
from rotiseria.models.pedido import Pedido

class PedidoProducto (models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    precioVariable = models.DecimalField(max_digits=7, decimal_places=2, default = 0, null=False, blank=False)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, default = 0, null=False, blank=False)
    cantidad = models.PositiveIntegerField(blank=False)

    def generarSubtotal (self):
        self.subtotal = Producto.getPrecioActual() * self.cantidad

    def getSubtotal (self):
        return self.subtotal
