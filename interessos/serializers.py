from rest_framework import serializers
from .models import InteresEnEsdeveniment, InteresEnTematica, InteresEnValoracio


class InteresEnEsdevenimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteresEnEsdeveniment
        fields = ('id', 'perfil', 'esdeveniment')


class InteresEnTematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteresEnTematica
        fields = ('id', 'perfil', 'tematica')

class InteresEnValoracioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteresEnValoracio
        fields = ('id', 'perfil', 'valoracio')