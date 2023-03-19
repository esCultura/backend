from django.contrib import admin
from . import models


@admin.register(models.Esdeveniment)
class Esdeveniment(admin.ModelAdmin):
    pass
