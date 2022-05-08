from datetime import datetime
from django.db import models
from usuarios.models import Usuarios


class Arquivo(models.Model):
    dia_da_transacao = models.DateField()
    horario_import = models.DateTimeField(default=datetime.now(), null=False)
    nome_usuario = models.TextField(max_length=100)

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
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    nome_usuario = models.TextField(max_length=100)
    arquivo = models.ForeignKey(Arquivo, on_delete=models.CASCADE)
    
