from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

from .models import Perfil, Organitzador, Administrador



class PerfilSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source = "user.email")
    username = serializers.CharField(source = "user.username")

    class Meta:
        model = Perfil
        fields = ('user', 'email', 'username', 'imatge')

class OrganitzadorSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source = "user.email")
    username = serializers.CharField(source = "user.username")

    class Meta:
        model = Organitzador
        fields = ('user', 'email', 'username', 'descripcio', 'url', 'telefon')

class AdministradorSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source = "user.email")
    username = serializers.CharField(source = "user.username")

    class Meta:
        model = Administrador
        fields = ('user', 'email', 'username')


class LoginPerfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("No existeix un usuari amb aquest username.")
        
        pwd_valid = check_password(password, user.password)

        if not pwd_valid:
            raise serializers.ValidationError("Contrasenya incorrecta.")
        
        self.context['user'] = user
        
        return data
    
    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        data['token'] = token.key
        return data


class SignUpPerfilsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        Perfil.objects.create(user=user)

        return user