from django.contrib import admin
from . import models


@admin.register(models.AssistenciaAEsdeveniment)
class AssistenciaAEsdeveniment(admin.ModelAdmin):
    pass