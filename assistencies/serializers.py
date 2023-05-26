from rest_framework import serializers
from .models import AssistenciaAEsdeveniment
from .qr import genera_image_data_qr
from escultura import settings


class AssistenciaAEsdevenimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistenciaAEsdeveniment
        fields = ('uuid', 'perfil', 'esdeveniment', 'data', 'dataValidacio')


class EntradaSerializer(serializers.ModelSerializer):
    qr = serializers.SerializerMethodField(read_only=True)
    foto = serializers.SerializerMethodField(read_only=True)
    esdeveniment = serializers.SerializerMethodField(read_only=True)
    data = serializers.SerializerMethodField(read_only=True)
    hora = serializers.SerializerMethodField(read_only=True)
    nom = serializers.SerializerMethodField(read_only=True)

    def get_qr(self, assistencia):
        return genera_image_data_qr(settings.FRONTEND_URL + '/checkin/' + str(assistencia.uuid))

    def get_foto(self, assistencia):
        return assistencia.esdeveniment.get_imatges()[0]

    def get_esdeveniment(self, assistencia):
        return assistencia.esdeveniment.nom

    def get_data(self, assistencia):
        return assistencia.data.strftime("%d / %m / %Y")

    def get_hora(self, assistencia):
        return "20:00h"

    def get_nom(self, assistencia):
        return assistencia.perfil.user.username

    class Meta:
        model = AssistenciaAEsdeveniment
        fields = ('qr', 'foto', 'esdeveniment', 'data', 'hora', 'nom')
