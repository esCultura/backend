from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from usuaris import permissions
from .models import Valoracio
from .serializers import ValoracioSerializer


class ValoracionsView(viewsets.ModelViewSet):
    queryset = Valoracio.objects.all()
    serializer_class = ValoracioSerializer
    permission_classes = [permissions.IsPerfil]

    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = {
        'esdeveniment__codi': ['exact', 'in'],
        'creador__user__id': ['exact', 'in']
    }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['creador_id'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
