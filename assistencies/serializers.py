from rest_framework import serializers
from .models import AssistenciaAEsdeveniment


class AssistenciaAEsdevenimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistenciaAEsdeveniment
        fields = ('id', 'perfil', 'esdeveniment', 'data')