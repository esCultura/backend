from rest_framework import viewsets

from django.contrib.auth.models import User
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from requests.exceptions import HTTPError

from social_django.utils import psa

from usuaris import permissions
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .models import Perfil, Organitzador, Administrador
from .serializers import PerfilSerializer, OrganitzadorSerializer, AdministradorSerializer, SignUpPerfilsSerializer, SignUpOrganitzadorsSerializer, SignUpAdminSerializer, LoginPerfilSerializer, LoginOrganitzadorSerializer, LoginAdminSerializer


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

    @action(methods=['GET', 'PUT'], detail=False)
    def jo(self, request):

        if self.request.auth is None:
            return Response(status=400, data={'error': 'No authentication token was provided.'})

        user = Token.objects.get(key=self.request.auth.key).user
        message = 'Els atributs que es poden modificar són: [password, imatge, bio]'

        if request.method == 'PUT':
            newPassword = request.data.get('password', None)
            newImage = request.data.get('imatge', None)
            newBio = request.data.get('bio', None)

            elementsModificats = []
            if newPassword is not None:
                user.set_password(newPassword)
                elementsModificats.append("password")
            if newImage is not None:
                user.perfil.imatge = newImage
                elementsModificats.append("imatge")
            if newBio is not None:
                user.perfil.bio = newBio
                elementsModificats.append("bio")
            message = 'S\'ha actualitzat els atributs: [' + ", ".join(elementsModificats) + "]"
            if not elementsModificats:
                message = 'No s\'ha actualitzat cap atribut del perfil.'
            user.save()
            user.perfil.save()

        serializer = PerfilSerializer(user.perfil)
        return Response(status=200, data={**serializer.data, **{'message': message}})


class OrganitzadorView(viewsets.ModelViewSet):
    queryset = Organitzador.objects.all()
    serializer_class = OrganitzadorSerializer

class AdmistradorView(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class LoginPerfilsView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = LoginPerfilSerializer

class LoginOrganitzadorsView(viewsets.ModelViewSet):
    queryset = Organitzador.objects.all()
    serializer_class = LoginOrganitzadorSerializer

class LoginAdminView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginAdminSerializer

class SignUpPerfilsView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = SignUpPerfilsSerializer

class SignUpOrganitzadorsView(viewsets.ModelViewSet):
    queryset = Organitzador.objects.all()
    serializer_class = SignUpOrganitzadorsSerializer

class SignUpAdminsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpAdminSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def GoogleSignIn(request, backend):
    token = request.POST.get('access_token', None)
    if token is None:
        return Response(status=400, data={'error': 'No access_token was provided, you can provide it through an access_token parameter in the body of the request.'})
    try:
        user = request.backend.do_auth(token)
    except HTTPError as e:
        return Response(status=400, data={'errors': {'token': 'Invalid token', 'detail': str(e)}})


    if user:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            if user.perfil is None:
                Perfil.objects.create(user=user)
            serializer = PerfilSerializer(user.perfil)
            return Response(status=200, data={**serializer.data, 'token': token.key, 'created': created})
        return Response(status=400, data={'errors': 'User deleted their account or was banned by an administrator.'})

    else:
        return Response(status=400, data={'errors': {'token': 'Invalid token'}})



def enviarEmail(request, email_to, assumpte, titol, veredicte, missatge_final):
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS
        ) as connection:

        # Això és per evitar que cada cop que es corrin els tests s'enviïn correus
        enviar_email = True if request.POST.get('enviar_email', None) is None else False

        if enviar_email:
            html_content = render_to_string("email_template.html", {'title': titol, 'email_to': email_to[0], 'resolution': veredicte, 'final_message': missatge_final})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(assumpte, text_content, settings.EMAIL_HOST_USER, email_to, connection=connection)
            msg.attach_alternative(html_content, "text/html")
            msg.send()


class OrganitzadorsPendentsDeConfirmacioView(viewsets.ModelViewSet):
    queryset = Organitzador.objects.filter(user__is_active = False)
    serializer_class = OrganitzadorSerializer
    http_method_names = ['get', 'post']

    permission_classes = [permissions.IsAdmin]

    @action(methods=['GET', 'POST'], detail=True)
    def accept(self, request, pk):

        organitzador = Organitzador.objects.get(user=pk)
        message = 'Aquest organitzador està pendent de confirmació'

        if request.method == 'POST':
            enviarEmail(request, [organitzador.user.email, ], "Activació compte d\'organitzador a esCultura", "Enhorabona!", "APROVAT", "A partir d'ara podràs iniciar sessió i utilitzar la pàgina web per organitzar els teus esdeveniments.")

            organitzador.user.is_active = True
            organitzador.user.save()

            message = "Aquest organitzador ha estat verificat i serà notificat mitjançant un correu electrònic."

        serializer = self.serializer_class(organitzador)
        return Response(status=200, data={**serializer.data, **{'message': message}})

    @action(methods=['GET', 'POST'], detail=True)
    def reject(self, request, pk):

        organitzador = Organitzador.objects.get(user=pk)
        message = 'Aquest organitzador està pendent de confirmació'

        if request.method == 'POST':
            organitzador.delete()

            enviarEmail(request, [organitzador.user.email, ], "Rebutjament compte d\'organitzador a esCultura","Ho sentim!", "REBUTJAT", "El teu compte no compleix el criteris per poder formar part d'esCultura. :(")

            message = "Aquest organitzador ha estat rebutjat i serà notificat mitjançant un correu electrònic."

        serializer = self.serializer_class(organitzador)
        return Response(status=200, data={**serializer.data, **{'message': message}})
