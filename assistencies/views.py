from rest_framework import viewsets

from .models import AssistenciaAEsdeveniment
from .serializers import AssistenciaAEsdevenimentSerializer


class AssistenciaAEsdevenimentView(viewsets.ModelViewSet):
    queryset = AssistenciaAEsdeveniment.objects.all()
    serializer_class = AssistenciaAEsdevenimentSerializer