from django.db import models
from django.utils.translation import gettext_lazy as _
from usuaris.models import Perfil


# Xat pot ser individual o grupal. Té nom en cas que sigui grupal.
class Xat(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    nom = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Nom'))
    participants = models.ManyToManyField(Perfil, related_name='xats',  verbose_name=_('Participants'))
    dataCreacio = models.DateTimeField(auto_now_add=True, verbose_name=_('Data creació'))

    @property
    def ultim_missatge(self):
        try:
            return self.missatges.order_by('-data')[0]
        except IndexError:
            return None


class Missatge(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    xat = models.ForeignKey(Xat, related_name='missatges', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Xat'))
    creador = models.ForeignKey(Perfil, related_name='missatges', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Creador'))
    text = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Text'))
    data = models.DateTimeField(auto_now_add=True, verbose_name=_('Data creació'))
