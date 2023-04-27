import datetime
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from usuaris.permissions import IsAdminOrOrganitzadorEditPerfilRead

from .models import Esdeveniment
from .serializers import EsdevenimentSerializer
from .mixins import FilterBackend, PaginationClass


class EsdevenimentsView(viewsets.ModelViewSet):
    queryset = Esdeveniment.objects.all()
    pagination_class = PaginationClass
    serializer_class = EsdevenimentSerializer
    models = Esdeveniment
    permission_classes = [IsAdminOrOrganitzadorEditPerfilRead]

    filter_backends = [FilterBackend, DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'codi': ['exact', 'in'],
        'nom': ['exact', 'in', 'contains'],
        'dataIni': ['exact', 'range'],
        'dataFi': ['exact', 'range'],
        'descripcio': ['contains'],
        'entrades': ['isnull'],
        'horari': ['isnull'],
        'enllacos': ['isnull'],
        'imatges': ['isnull'],
        'provincia': ['exact', 'in'],
        'comarca': ['exact', 'in'],
        'municipi': ['exact', 'in'],
        'espai': ['exact', 'isnull'],
        'email': ['isnull'],
        'telefon': ['isnull'],
        'url': ['isnull'],
        'tematiques__nom': ['in'],
        'organitzador__user__first_name': ['exact', 'in', 'contains']
    }
    search_fields = ['nom', 'descripcio', 'provincia', 'comarca', 'municipi', 'espai']
    ordering_fields = ['codi', 'nom', 'dataIni', 'dataFi', 'provincia', 'comarca', 'municipi', 'latitud', 'longitud',
                       'espai', 'assistents', 'interessats']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(assistents=Count('assistencies'))
        if getattr(self.request.user, 'organitzador', False):
            return queryset.filter(organitzador=self.request.user.organitzador)
        else:
            return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description=_('Màxim nombre de resultats que es volen obtenir (per defecte=1000)'),
            ),
            openapi.Parameter(
                'latitud', openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                description=_('Latitud propera dels esdeveniments a retornar'),
            ),
            openapi.Parameter(
                'longitud', openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                description=_('Longitud propera dels esdeveniments a retornar'),
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Posem com a organitzador qui l'està creant si és organitzador. Si és admin, un id petit
        # I posem codi a l'esdeveniment seguint el següent patró:
        #   id de l'usuari + data d'avui + # d'esdeveniments creats per l'organitzador
        request.POST._mutable = True
        user_id = request.user.id
        avui = datetime.datetime.now().strftime("%Y%m%d")
        if getattr(request.user, 'organitzador', False):
            last = Esdeveniment.objects.filter(organitzador=request.user.organitzador).order_by('-codi').first()
            max_codi = 0
            if last:
                max_codi = (last.codi % pow(10, len(str(last.codi)) - (len(str(request.user.id)) + 8))) + 1
            codi = int(str(user_id) + avui + str(max_codi))
            request.POST['organitzador'] = user_id
        else:
            codi = Esdeveniment.objects.all().order_by('codi').first().codi - 1
        request.POST['codi'] = codi
        print(request.POST['codi'])
        response = super().create(request)
        request.POST._mutable = False
        return response
