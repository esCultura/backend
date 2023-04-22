from rest_framework import serializers

from .models import Esdeveniment, Tematica


class TematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tematica
        fields = '__all__'


class EsdevenimentSerializer(serializers.ModelSerializer):
    # Els camps enllacos, imatges i url els tenim guardats com un string amb diferents
    # valors separats per comes. Els serialitzem com una llista de tals valors
    enllacos_list = serializers.ListField(read_only=True, required=False, source='get_enllacos')
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatges')
    url_list = serializers.ListField(read_only=True, required=False, source='get_url')

    codi = serializers.IntegerField(required=False)
    tematiques = TematicaSerializer(many=True, required=False, read_only=True)
    tematiques_nom = serializers.PrimaryKeyRelatedField(
        queryset=Tematica.objects.all(),
        source='tematiques',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Esdeveniment
        fields = '__all__'
