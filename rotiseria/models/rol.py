from django.db import models

class Rol (models.Model):
    nombre = models.CharField (max_length=15)

    def __str__(self):
        return self.nombre