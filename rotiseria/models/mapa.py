from django.db import models

class Mapa(models.Model):
    latitud   = models.CharField(max_length=50, null=True)
    longitud  = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.direccion
    

