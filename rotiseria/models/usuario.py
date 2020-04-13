from django.db import models
from rotiseria.models.rol import Rol
from django.contrib.auth.models import User

class Usuario (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = (
            ('es_admin', 'Es_Admin'),
            ('es_repart', 'Es_Repart'),
            ('es_recep', 'Es_Recep'),
        )

