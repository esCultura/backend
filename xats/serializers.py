from rest_framework import serializers

from .models import Xat, Missatge


class XatSerializer(serializers.ModelSerializer):
    ultim_missatge = serializers.SerializerMethodField(read_only=True)

    def get_ultim_missatge(self, xat):
        ultim_missatge = xat.ultim_missatge
        if ultim_missatge:
            return MissatgeSerializer(xat.ultim_missatge).data
        else:
            return None

    class Meta:
        model = Xat
        fields = '__all__'


class MissatgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missatge
        fields = '__all__'