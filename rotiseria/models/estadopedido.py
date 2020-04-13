from django.db import models

class EstadoPedido (models.Model):
    estado = models.CharField(max_length=40)
    # pendiente: listo para aceptar o rechazar
    # confirmado: cuando el recepcionista lo acepta
    # rechazado: es cuando el recepcionita lo rechaza
    # listo: pedidos listos para ser entregados
    # enviado: se envian los pedidos listos al repartidor
    # entregado: el pedido fue entregado en el local o en domicilio

    def __str__(self):
        return str(self.estado)