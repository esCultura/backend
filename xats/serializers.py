from rest_framework import serializers

from .models import Xat, Missatge


class XatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xat
        fields = '__all__'


class MissatgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missatge
        fields = '__all__'