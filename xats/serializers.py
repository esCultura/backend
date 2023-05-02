from rest_framework import serializers
from usuaris.serializers import PerfilSerializer
from usuaris.models import Perfil
from .models import Xat, Missatge


class XatSerializer(serializers.ModelSerializer):
    ultim_missatge = serializers.SerializerMethodField(read_only=True)
    participants = PerfilSerializer(many=True, read_only=True)
    participant_id = serializers.PrimaryKeyRelatedField(
        queryset=Perfil.objects.all(),
        source='participants',
        many=True,
        write_only=True,
        required=False
    )

    def get_ultim_missatge(self, xat):
        ultim_missatge = xat.ultim_missatge
        if ultim_missatge:
            return MissatgeSerializer(xat.ultim_missatge).data
        else:
            return None

    class Meta:
        model = Xat
        fields = ('id', 'nom', 'participants', 'ultim_missatge', 'participant_id')


class MissatgeSerializer(serializers.ModelSerializer):
    creador = PerfilSerializer(read_only=True)
    creador_id = serializers.PrimaryKeyRelatedField(
        queryset=Perfil.objects.all(),
        source='creador',
        write_only=True
    )
    xat_id = serializers.PrimaryKeyRelatedField(
        queryset=Xat.objects.all(),
        source='xat',
        write_only=True
    )

    class Meta:
        model = Missatge
        fields = ('text', 'data', 'creador', 'creador_id', 'xat_id')
