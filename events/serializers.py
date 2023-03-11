from rest_framework import serializers

from .models import Esdeveniment


class EsdevenimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Esdeveniment
        fields = ('codi', 'nom', 'dataIni', 'dataFi', 'descripcio')

