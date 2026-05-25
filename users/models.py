from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuário customizado.
    Estende o AbstractUser do Django, que já fornece:
    - password (com hash automático via PBKDF2 — seguro equivalente ao bcrypt)
    - is_active, is_staff, is_superuser
    - date_joined, last_login
    - métodos de autenticação prontos

    Campos customizados:
    - name: nome do usuário (substitui username)
    - email: usado como identificador único de login
    """
    # Desativa o campo username padrão do AbstractUser
    username = None

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    # Login feito por e-mail, não por username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
