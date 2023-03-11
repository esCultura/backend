from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin

from .models import Esdeveniment
from .serializers import EsdevenimentSerializer


# Create your views here.
class EsdevenimentsView(viewsets.ModelViewSet):
    queryset = Esdeveniment.objects.all()
    serializer_class = EsdevenimentSerializer
    models = Esdeveniment
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Esdeveniment.obects.get_object_or_404(codi=self.request.codi)

