from django.contrib import admin
from . import models


@admin.register(models.Valoracio)
class Valoracio(admin.ModelAdmin):
    pass
