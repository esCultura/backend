from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Xat
from .serializers import XatSerializer


class XatsView(viewsets.ModelViewSet):
    queryset = Xat.objects.all()
    serializer_class = XatSerializer
    model = Xat
    permission_classes = []

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ['exact', 'in'],
        'nom': ['exact', 'in'],
        'participants__username': ['in'],
        'dataCreacio': ['exact', 'range'],
    }
