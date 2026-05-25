from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserRegistrationSerializer, UserDetailSerializer


class UserRegistrationView(CreateAPIView):
    """
    POST /api/users/register/

    Cadastra um novo usuário.
    Endpoint público (AllowAny) — nenhum token necessário.

    Body esperado:
        {
            "name": "João Silva",
            "email": "joao@email.com",
            "password": "SenhaForte@123",
            "password2": "SenhaForte@123"
        }

    Resposta de sucesso (201 Created):
        {
            "message": "Usuário cadastrado com sucesso.",
            "user": {
                "id": 1,
                "name": "João Silva",
                "email": "joao@email.com",
                "date_joined": "2024-01-01T00:00:00Z"
            }
        }

    Erros retornados (400 Bad Request):
        - E-mail já cadastrado
        - Senhas não coincidem
        - Senha fraca (muito curta, muito comum, etc.)
        - Campos obrigatórios ausentes
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            "message": "Usuário cadastrado com sucesso.",
            "user": UserDetailSerializer(user).data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
