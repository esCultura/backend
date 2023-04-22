from django.contrib import admin
from . import models


@admin.register(models.Seguiment)
class Seguiment(admin.ModelAdmin):
    pass