from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Seguiment(models.Model):
    seguidor = models.ForeignKey('usuaris.Perfil', related_name='seguits', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Perfil seguidor'))
    seguit = models.ForeignKey('usuaris.Perfil', related_name='seguidors', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Perfil seguit'))

    class Meta:
        unique_together = ('seguidor', 'seguit')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(seguidor=models.F('seguit')),
                name='no_es_pot_seguir_a_un_mateix'
            ),
        ]