from datetime import datetime
from operator import mod
from django.db import models
from usuarios.models import Usuarios

class Transacao(models.Model):
    banco_emissor = models.TextField(max_length=200)
    agencia_banco_emissor = models.TextField(max_length=10)
    numero_banco_emissor = models.TextField(max_length=20)
    banco_destinatario = models.TextField(max_length=200)
    agencia_banco_destinatario = models.TextField(max_length=10)
    numero_banco_destinatario = models.TextField(max_length=20)
    valor_transacao = models.FloatField(null=False, blank=False)
    dia_da_transacao = models.DateField()
    horario_import = models.DateTimeField(default=datetime.now(), null=False)
    desativado = models.BooleanField(default=False)
    
