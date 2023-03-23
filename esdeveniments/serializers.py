from rest_framework import serializers

from .models import Esdeveniment


class EsdevenimentSerializer(serializers.ModelSerializer):
    # Els camps enllacos, imatges i url els tenim guardats com un string amb diferents
    # valors separats per comes. Els serialitzem com una llista de tals valors
    enllacos_list = serializers.ListField(read_only=True, required=False, source='get_enllacos')
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatges')
    url_list = serializers.ListField(read_only=True, required=False, source='get_url')

    class Meta:
        model = Esdeveniment
        fields = '__all__'
