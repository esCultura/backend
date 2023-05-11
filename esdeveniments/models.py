from django.db import models
from usuaris.models import Organitzador
from django.utils.translation import gettext_lazy as _


def split_or_none(attr):
    if attr:
        return attr.split(',')
    else:
        return None


class Tematica(models.Model):
    nom = models.CharField(primary_key=True, max_length=100, verbose_name=_('Nom'))
    descripcio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Descripció'))

    class Meta:
        # Per defecte, el nom és "Tematicas", el sobreescrivim
        verbose_name_plural = _('Temàtiques')


class Esdeveniment(models.Model):
    codi = models.BigIntegerField(primary_key=True, verbose_name=_('Codi'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    dataIni = models.DateTimeField(null=True, blank=True, verbose_name=_('Data inici'))
    dataFi = models.DateTimeField(null=True, blank=True, verbose_name=_('Data fi'))
    descripcio = models.CharField(max_length=10000, null=True, blank=True, verbose_name=_('Descripció'))
    tematiques = models.ManyToManyField(Tematica)
    entrades = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Entrades'))
    horari = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Horari'))
    enllacos = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Enllaços'))
    imatges = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Imatges'))
    provincia = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Província'))
    comarca = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Comarca'))
    municipi = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Municipi'))
    latitud = models.FloatField(null=True, blank=True, verbose_name=_('Latitud'))
    longitud = models.FloatField(null=True, blank=True, verbose_name=_('Longitud'))
    espai = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Espai'))
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name=_('Email contacte'))
    telefon = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Telèfon contacte'))
    url = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('URL organitzador'))
    organitzador = models.ForeignKey(Organitzador, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name=_('Organitzador'))
    reports = models.CharField(max_length=1000, null=True, blank=True, default="", verbose_name=_('Usuaris que han reportat l\'esdeveniment'))

    def get_enllacos(self):
        return split_or_none(self.enllacos)

    def get_imatges(self):
        imatges = split_or_none(self.imatges)
        if imatges:
            imatges_url = []
            for imatge in imatges:
                ini = imatge.split('://')[0]
                if ini != 'http' and ini != 'https':
                    imatges_url.append('http://agenda.cultura.gencat.cat' + imatge)
                else:
                    imatges_url.append(imatge)
            return imatges_url
        return imatges

    def get_url(self):
        return split_or_none(self.url)

    def get_reports(self):
        reports = split_or_none(self.reports)
        return reports if reports is not None else []

    def get_num_reports(self):
        reports = split_or_none(self.reports)
        return len(reports) if reports is not None else 0