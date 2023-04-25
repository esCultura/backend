from rest_framework import serializers
from .models import Seguiment


class SeguimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguiment
        fields = ('id', 'seguidor', 'seguit')