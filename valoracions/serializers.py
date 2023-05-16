from rest_framework import serializers
from usuaris.serializers import PerfilSerializer
from usuaris.models import Perfil
from .models import Valoracio


class ValoracioSerializer(serializers.ModelSerializer):
    creador = PerfilSerializer(read_only=True)
    creador_id = serializers.PrimaryKeyRelatedField(
        queryset=Perfil.objects.all(),
        write_only=True,
        source='creador'
    )

    class Meta:
        model = Valoracio
        fields = '__all__'
