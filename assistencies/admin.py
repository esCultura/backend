from django.contrib import admin
from .models import AssistenciaAEsdeveniment


@admin.register(AssistenciaAEsdeveniment)
class AssistenciaAEsdeveniment(admin.ModelAdmin):
    pass