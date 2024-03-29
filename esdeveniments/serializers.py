from rest_framework import serializers
from django.db.models import Avg
import random

from .models import Esdeveniment, Tematica


class TematicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tematica
        fields = '__all__'


class EsdevenimentSerializer(serializers.ModelSerializer):
    # Els camps enllacos, imatges i url els tenim guardats com un string amb diferents
    # valors separats per comes. Els serialitzem com una llista de tals valorsPROVA
    enllacos_list = serializers.ListField(read_only=True, required=False, source='get_enllacos')
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatges')
    url_list = serializers.ListField(read_only=True, required=False, source='get_url')

    num_reports = serializers.IntegerField(read_only=True, required=False, source='get_num_reports')

    codi = serializers.IntegerField(required=False)
    tematiques = TematicaSerializer(many=True, required=False, read_only=True)
    tematiques_nom = serializers.PrimaryKeyRelatedField(
        queryset=Tematica.objects.all(),
        source='tematiques',
        many=True,
        write_only=True,
        required=False
    )
    puntuacio = serializers.SerializerMethodField(read_only=True)

    # Per petició de l'equip de mobilitat (serveis externs), afegim camps punts i descompte
    # Valor random entre 20 i 250, sempre el mateix
    punts = serializers.SerializerMethodField(read_only=True)

    # Valor random dins el conjunt {10, 15, 20, 25, 50}, sempre el mateix
    descompte = serializers.SerializerMethodField(read_only=True)

    def get_puntuacio(self, esdeveniment):
        mitjana = esdeveniment.valoracions.aggregate(mitjana=Avg('puntuacio'))['mitjana']
        if mitjana:
            return round(mitjana, 2)
        else:
            return None

    def get_punts(self, esdeveniment):
        # Fem set de la seed per obtenir sempre el mateix random donat aquell esdeveniment
        random.seed(esdeveniment.codi)

        # Generem random entre 20 i 250
        return random.randint(20, 250)

    def get_descompte(self, esdeveniment):
        # Fem set de la seed per obtenir sempre el mateix random donat aquell esdeveniment
        random.seed(esdeveniment.codi)

        # Generem random dins el conjunt {10, 15, 20, 25, 50}
        return random.choice([10, 15, 20, 25, 50])

    class Meta:
        model = Esdeveniment
        fields = '__all__'
