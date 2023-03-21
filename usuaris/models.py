from django.db import models
from django.utils.translation import gettext_lazy as _


class Perfil(models.Model):
    username = models.CharField(primary_key=True, max_length=20, verbose_name=_('Nom d''usuari'))
