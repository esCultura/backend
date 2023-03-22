from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class AssistenciaAEsdeveniment(models.Model):
    perfil = models.ForeignKey('usuaris.Perfil', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Username perfil'))
    esdeveniment = models.ForeignKey('esdeveniments.Esdeveniment', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Codi esdeveniment'))

    # Afegim una constraint per tal que no es pugui repetir
    # la combinació d'un perfil i un esdeveniment determinats.
    class Meta:
        unique_together = ('perfil', 'esdeveniment')