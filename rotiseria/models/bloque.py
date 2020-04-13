from django.db import models
from datetime import datetime

class Bloque(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default = datetime.now)
   
    def __str__(self):
        return str(self.id)     