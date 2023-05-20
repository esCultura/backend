from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class InteresEnEsdeveniment(models.Model):
    perfil = models.ForeignKey('usuaris.Perfil', related_name='interessos_esdeveniment', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Id perfil'))
    esdeveniment = models.ForeignKey('esdeveniments.Esdeveniment', related_name='interessats', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Codi esdeveniment'))

    # Afegim una constraint per tal que no es pugui repetir
    # la combinació d'un perfil i un esdeveniment determinats.
    class Meta:
        unique_together = ('perfil', 'esdeveniment')


class InteresEnTematica(models.Model):
    perfil = models.ForeignKey('usuaris.Perfil', related_name='interessos_tematica', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Id perfil'))
    tematica = models.ForeignKey('esdeveniments.Tematica', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Nom tematica'))

    # Afegim una constraint per tal que no es pugui repetir
    # la combinació d'un perfil i una tematica determinats.
    class Meta:
        unique_together = ('perfil', 'tematica')

class InteresEnValoracio(models.Model):
    perfil = models.ForeignKey('usuaris.Perfil', related_name='interessos_valoracio', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Id perfil'))
    valoracio = models.ForeignKey('valoracions.Valoracio', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Id valoració'))

    # Afegim una constraint per tal que no es pugui repetir
    # la combinació d'un perfil i una valoracio determinats.
    class Meta:
        unique_together = ('perfil', 'valoracio')