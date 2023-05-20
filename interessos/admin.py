from django.contrib import admin
from . import models


@admin.register(models.InteresEnEsdeveniment)
class InteresEnEsdeveniment(admin.ModelAdmin):
    pass

@admin.register(models.InteresEnTematica)
class InteresEnTematica(admin.ModelAdmin):
    pass

@admin.register(models.InteresEnValoracio)
class InteresEnValoracio(admin.ModelAdmin):
    pass