import email
from django.db import models
from django.contrib.auth.models import User


class Usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.TextField(max_length=100)
    email = models.TextField(max_length=200)
    admin = models.BooleanField(default=True)
    senha = models.TextField(max_length=100)
    desativado = models.BooleanField(default=False)

