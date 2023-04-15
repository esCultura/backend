from rest_framework import viewsets
from .models import Xat
from .serializers import XatSerializer


class XatsView(viewsets.ModelViewSet):
    queryset = Xat.objects.all()
    serializer_class = XatSerializer
    model = Xat
    permission_classes = []
