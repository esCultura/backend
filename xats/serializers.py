from rest_framework import serializers

from .models import Xat


class XatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xat
        fields = '__all__'
