from django.db import models
from rotiseria.models.categoría import Categoría

class Producto(models.Model):
    
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50, blank=True)
    foto = models.ImageField(upload_to="rotiseria/images/", null=True)
    precioActual = models.DecimalField(max_digits=8, decimal_places=2)
    categoria= models.ForeignKey(Categoría, on_delete=models.CASCADE)
    ganancia= models.IntegerField(null=True)

    def __str__(self):
        return self.nombre

    def getPrecioActual(self):
        return self.precioActual
