from django.contrib import admin
from . import models


@admin.register(models.Esdeveniment)
class Esdeveniment(admin.ModelAdmin):
    pass


@admin.register(models.Tematica)
class Tematica(admin.ModelAdmin):
    pass
