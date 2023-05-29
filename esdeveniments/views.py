import datetime
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db.models import Count, Avg
from django.utils.translation import gettext_lazy as _

from usuaris.permissions import IsAdminOrOrganitzadorEditOthersRead

from .models import Esdeveniment
from .serializers import EsdevenimentSerializer
from .mixins import FilterBackend, PaginationClass

from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

class EsdevenimentsView(viewsets.ModelViewSet):
    queryset = Esdeveniment.objects.all()
    pagination_class = PaginationClass
    serializer_class = EsdevenimentSerializer
    models = Esdeveniment
    permission_classes = [IsAdminOrOrganitzadorEditOthersRead]


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
                       'espai', 'assistents', 'likes', 'puntuacio']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(assistents=Count('assistencies'))
        queryset = queryset.annotate(likes=Count('interessats'))
        queryset = queryset.annotate(puntuacio=Avg('valoracions__puntuacio'))
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
        data = request.data.copy()
        user_id = request.user.id
        avui = datetime.datetime.now().strftime("%Y%m%d")
        if getattr(request.user, 'organitzador', False):
            last = Esdeveniment.objects.filter(organitzador=request.user.organitzador).order_by('-codi').first()
            max_codi = 0
            if last:
                max_codi = (last.codi % pow(10, len(str(last.codi)) - (len(str(request.user.id)) + 8))) + 1
            codi = int(str(user_id) + avui + str(max_codi))
            data['organitzador'] = user_id
        else:
            codi = Esdeveniment.objects.all().order_by('codi').first().codi - 1
        data['codi'] = codi
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=True)
    def report(self, request, pk):
        if self.request.auth is None:
            return Response(status=400, data={'error': 'No authentication token was provided.'})
        user = Token.objects.get(key=self.request.auth.key).user
        esdeveniment = self.get_object()
        reports = esdeveniment.get_reports()
        if user.username in reports:
            return Response(status=400, data={'error': 'Ja has reportat aquest esdeveniment anteriorment.'})
        if len(reports) == 4:
            esdeveniment.delete()
            return Response(status=200, data={'message': 'Has reportat correctament l\'esdeveniment. L\'esdeveniment ha estat reportat tantes vegades que s\'ha eliminat.'})
        else:
            if not reports: esdeveniment.reports = user.username
            else: esdeveniment.reports = ",".join(reports) + "," + user.username
            esdeveniment.save()
            return Response(status=200, data={'message': 'Has reportat correctament l\'esdeveniment.'})