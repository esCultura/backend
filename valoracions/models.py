from django.db import models
from django.utils.translation import gettext_lazy as _
from usuaris.models import Perfil
from esdeveniments.models import Esdeveniment


class Valoracio(models.Model):
    TPuntuacio = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )

    id = models.AutoField(primary_key=True, verbose_name=_('Identidicador'))
    data = models.DateTimeField(auto_now_add=True, verbose_name=_('Data creació'))
    text = models.CharField(max_length=10000, verbose_name=_('Text'))
    puntuacio = models.IntegerField(choices=TPuntuacio)
    creador = models.ForeignKey(Perfil, related_name='valoracions', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Creador'))
    esdeveniment = models.ForeignKey(Esdeveniment, related_name='valoracions', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Esdeveniment'))

    class Meta:
        # Per defecte, el nom és "Valoracios", el sobreescrivim
        verbose_name_plural = _('Valoracions')
