from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

from .models import Perfil, Organitzador, Administrador



class PerfilSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source = "user.email", read_only=True)
    username = serializers.CharField(source = "user.username", read_only=True)
    password = serializers.CharField(source="user.password", required=False, write_only=True)

    class Meta:
        model = Perfil
        fields = ('user', 'email', 'username', 'password', 'imatge', 'bio', 'estadistiques')


class OrganitzadorSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source = "user.email", read_only=True)
    username = serializers.CharField(source = "user.username", read_only=True)

    class Meta:
        model = Organitzador
        fields = ('user', 'email', 'username', 'descripcio', 'url', 'telefon')

class AdministradorSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source = "user.email", read_only=True)
    username = serializers.CharField(source = "user.username", read_only=True)

    class Meta:
        model = Administrador
        fields = ('user', 'email', 'username')



def validacioLogin(data):
    username = data.get("user", None)
    if username is not None:
        username = username['username']
    else:
        username = data.get("username", None)
    password = data.get("password", None)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise serializers.ValidationError("No existeix un usuari amb aquest username.")

    if not user.is_active:
        raise serializers.ValidationError("Aquest usuari ha estat banejat o es troba pendent de confirmació.")

    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        raise serializers.ValidationError("Contrasenya incorrecta.")
    return user

def creacioLogin(data, user):
    token, created = Token.objects.get_or_create(user=user)
    data['token'] = token.key
    data['created'] = created
    return data

class LoginPerfilSerializer(PerfilSerializer):
    user = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    username = serializers.CharField(source = "user.username", max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    imatge = serializers.ImageField(required=False, read_only=True)
    bio = serializers.CharField(required=False, read_only=True)
    token = serializers.CharField(required=False, read_only=True)
    created = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = Perfil
        fields = ('user', 'email', 'username', 'imatge', 'bio', 'estadistiques', 'password', 'token', 'created')

    def validate(self, data):
        user = validacioLogin(data)
        try:
            _ = user.perfil
        except:
            raise serializers.ValidationError("No existeix un perfil amb aquest username.")
        self.context['user'] = user

        return data

    def create(self, data):
        user = self.context['user']
        data = creacioLogin(data, user)
        data['user'] = user
        data['email'] = user.email
        data['imatge'] = user.perfil.imatge
        data['bio'] = user.perfil.bio
        data['estadistiques'] = user.perfil.estadistiques
        return data

class LoginOrganitzadorSerializer(OrganitzadorSerializer):
    user = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    username = serializers.CharField(source = "user.username", max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    descripcio = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    telefon = serializers.CharField(read_only=True)
    token = serializers.CharField(required=False, read_only=True)
    created = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = Organitzador
        fields = ('user', 'email', 'username', 'password', 'descripcio', 'url', 'telefon', 'token', 'created')

    def validate(self, data):
        user = validacioLogin(data)
        try:
            _ = user.organitzador
        except:
            raise serializers.ValidationError("No existeix un organitzador amb aquest username.")
        self.context['user'] = user

        return data

    def create(self, data):
        user = self.context['user']
        data = creacioLogin(data, user)
        data['user'] = user
        data['email'] = user.email
        data['descripcio'] = user.organitzador.descripcio
        data['url'] = user.organitzador.url
        data['telefon'] = user.organitzador.telefon
        return data

class LoginAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(required=False, read_only=True)
    created = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token', 'created')

    def validate(self, data):
        user = validacioLogin(data)
        try:
            _ = user.administrador
        except:
            raise serializers.ValidationError("No existeix un administrador amb aquest username.")
        self.context['user'] = user

        return data

    def create(self, data):
        return creacioLogin(data, self.context['user'])



def validacioSignUp(data):
    if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
    return data

def creacioUsuari(data):
    print(data)
    user = data.get("user", None)
    if user is not None:
        username = user['username']
        email = user['email']
    else:
        username = data['username']
        email = data['email']
    user = User.objects.create(
            username=username,
            email=email,
        )
    user.is_active = True


    user.set_password(data['password'])
    user.save()

    token, created = Token.objects.get_or_create(user=user)
    data['token'] = token.key
    data['created'] = created

    return user, data

class SignUpPerfilsSerializer(PerfilSerializer):
    user = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.EmailField(
            source="user.email",
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(source = "user.username", max_length=255, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    imatge = serializers.ImageField(required=False, read_only=True)
    bio = serializers.CharField(required=False, read_only=True)
    token = serializers.CharField(required=False, read_only=True)
    created = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = Perfil
        fields = ('user', 'email', 'username', 'password', 'password2', 'imatge', 'bio', 'estadistiques', 'token', 'created')

    def validate(self, data):
        return validacioSignUp(data)

    def create(self, data):
        user, data = creacioUsuari(data)
        Perfil.objects.create(user=user)
        data['user'] = user
        data['imatge'] = user.perfil.imatge
        data['bio'] = user.perfil.bio
        data['estadistiques'] = user.perfil.estadistiques
        return data

class SignUpOrganitzadorsSerializer(OrganitzadorSerializer):
    user = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.EmailField(
            source="user.email",
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(source = "user.username", max_length=255, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    descripcio = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    telefon = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)

    class Meta:
        model = Organitzador
        fields = ('user', 'email', 'username', 'password', 'password2', 'descripcio', 'url', 'telefon', 'message')

    def validate(self, data):
        return validacioSignUp(data)

    def create(self, data):
        user, data = creacioUsuari(data)
        Organitzador.objects.create(user=user)
        user.is_active = False
        user.save()
        data['user'] = user
        data['descripcio'] = user.organitzador.descripcio
        data['url'] = user.organitzador.url
        data['telefon'] = user.organitzador.telefon
        data['message'] = "El teu compte està pendent d'aprovació, rebràs un correu quan un administrador et verifiqui."
        return data

class SignUpAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(required=False, read_only=True)
    created = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'token', 'created')

    def validate(self, data):
        return validacioSignUp(data)

    def create(self, data):
        user, data = creacioUsuari(data)
        Administrador.objects.create(user=user)
        return data