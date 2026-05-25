from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer para cadastro de usuário.
    - Valida e-mail único (já garantido pelo model, mas retorna mensagem clara)
    - Valida força da senha com as regras padrão do Django (PBKDF2 — seguro equivalente ao bcrypt)
    - Exige confirmação de senha (write_only, nunca retorna na resposta)
    - Cria o usuário com senha hasheada via create_user()
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirme a senha",
    )

    class Meta:
        model = User
        fields = ("id", "name", "email", "password", "password2")
        read_only_fields = ("id",)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "As senhas não coincidem."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            email=validated_data["email"].lower(),
            name=validated_data["name"],
            password=validated_data["password"],
        )
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer somente-leitura para retornar dados do usuário
    (usado na resposta após cadastro bem-sucedido).
    """
    class Meta:
        model = User
        fields = ("id", "name", "email", "date_joined")
