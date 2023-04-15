from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Perfil(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name=_('User'))
    imatge = models.ImageField(null=True, blank=True, verbose_name=_('Imatge de perfil'))

class Organitzador(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name=_('User'))
    descripcio = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('Descripció'))
    url = models.URLField(null=True, blank=True, verbose_name=_('URL'))
    telefon = models.CharField(max_length=9, null=True, blank=True, verbose_name=_('Telèfon'))

class Administrador(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)