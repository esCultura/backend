from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import datetime
import uuid


class AssistenciaAEsdeveniment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('Identificador'))
    perfil = models.ForeignKey('usuaris.Perfil', related_name='assistencies', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Id perfil'))
    esdeveniment = models.ForeignKey('esdeveniments.Esdeveniment', related_name='assistencies', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Codi esdeveniment'))
    data = models.DateTimeField(null=False, blank=False, default=datetime.now, verbose_name=_('Data assistencia'))

    # Afegim una constraint per tal que no es pugui repetir
    # la combinació d'un perfil i un esdeveniment determinats.
    class Meta:
        unique_together = ('perfil', 'esdeveniment')