from rest_framework import serializers
from .models import Perfil, Organitzador, Administrador


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ('id', 'email', 'username', 'imatge')

class OrganitzadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organitzador
        fields = ('id', 'email', 'descripcio', 'url', 'telefon')

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ('id', 'email')