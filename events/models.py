from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Esdeveniment(models.Model):
    codi = models.AutoField(primary_key=True, verbose_name=_('Codi'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    dataIni = models.DateTimeField(null=False, blank=False, verbose_name=_('Data inici'))
    dataFi = models.DateTimeField(null=False, blank=False, verbose_name=_('Data fi'))
    descripcio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Descripcio'))

