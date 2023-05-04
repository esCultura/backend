import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from escultura import settings


def get_default_imatge():
    return settings.DEFAULT_IMATGE_PERFIL


class Perfil(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name=_('User'))
    imatge = models.ImageField(null=True, blank=True, default=get_default_imatge(), verbose_name=_('Imatge de perfil'))
    bio = models.CharField(max_length=200, default="", null=True, blank=True, verbose_name=_('Bio'))

    def get_nombre_xats(self):
        return len(self.xats.all())

    @property
    def estadistiques(self):
        return {
            'xats_participant': len(self.xats.all()),
            'missatges_enviats': len(self.missatges.all()),
            'assistencies_passades': len(self.assistencies.filter(data__lt=datetime.datetime.now())),
            'reserves_futures': len(self.assistencies.filter(data__gt=datetime.datetime.now())),
            'interessos_esdeveniments': len(self.interessos_esdeveniment.all()),
            'interessos_tematiques': len(self.interessos_tematica.all()),
            'seguidors': len(self.seguidors.all()),
            'seguits': len(self.seguits.all())
        }


class Organitzador(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name=_('User'))
    descripcio = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('Descripció'))
    url = models.URLField(null=True, blank=True, verbose_name=_('URL'))
    telefon = models.CharField(max_length=9, null=True, blank=True, verbose_name=_('Telèfon'))

class Administrador(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)