from django.db import models

class Cliente(models.Model):
    nombre= models.CharField(max_length=50)
    telefono= models.IntegerField(primary_key=True)

    def __str__(self):
        return self.nombre