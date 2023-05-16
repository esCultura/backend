from rest_framework import viewsets
from .models import Valoracio
from .serializers import ValoracioSerializer


class ValoracionsView(viewsets.ModelViewSet):
    queryset = Valoracio.objects.all()
    serializer_class = ValoracioSerializer

