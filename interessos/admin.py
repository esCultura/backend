from django.contrib import admin
from .models import InteresEnEsdeveniment, InteresEnTematica


@admin.register(InteresEnEsdeveniment)
class InteresEnEsdeveniment(admin.ModelAdmin):
    pass

@admin.register(InteresEnTematica)
class InteresEnTematica(admin.ModelAdmin):
    pass