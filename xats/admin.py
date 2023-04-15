from django.contrib import admin
from . import models


@admin.register(models.Xat)
class Xat(admin.ModelAdmin):
    pass


@admin.register(models.Missatge)
class Missatge(admin.ModelAdmin):
    pass
