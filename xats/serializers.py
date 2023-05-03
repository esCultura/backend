from datetime import date
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
        fields = ('id', 'participants', 'ultim_missatge', 'participant_id')


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
    data = serializers.SerializerMethodField(read_only=True)

    def get_data(self, missatge):
        avui = date.today()
        data = missatge.data
        if data.date() < avui:
            # Si la data és anterior a avui
            return data.strftime('%H:%M %d-%m-%Y')
        else:
            # Si el missatge és d'avui
            return data.strftime('%H:%M')

    class Meta:
        model = Missatge
        fields = ('text', 'data', 'creador', 'creador_id', 'xat_id')
