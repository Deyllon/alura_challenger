from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.models import User
import bcrypt
from django.shortcuts import get_object_or_404




from usuarios.models import Usuarios

def gerar_senha():
    
    senha = ''
    contador = 0
    
    while contador <= 5:
        x = random.randint(0,9)
        senha+= str(x)
        contador+=1
    
    return senha

def encriptografar_senha(senha):
    
    senha_criptografada = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

    return senha_criptografada

def salvar_usuario(nome, email, senha):
    
    senha_criptografada = encriptografar_senha(senha)
    
    usuario = User.objects.create_user(username=nome, email= email, password= senha)

    usuario.save()
    
    usuario = Usuarios.objects.create(user=usuario, nome=usuario.username, email= usuario.email, admin=False, senha = senha_criptografada)
    
    usuario.save()
        
def pegar_usuarios(request):
    
    usuarios = Usuarios.objects.exclude(admin=True)& Usuarios.objects.exclude(user=request.user) & Usuarios.objects.exclude(desativado= True)
    
    return usuarios

def editar_usuario(pk, nome, email, senha):
    
    usuario = get_object_or_404(nome, email, senha)
    
    usuario.nome = nome
    usuario.email = email
    usuario.senha = encriptografar_senha(senha)
    
    usuario.save()
    
def pegar_usuario(pk):
    
    usuario = get_object_or_404(Usuarios, pk=pk)
    
    return usuario

def enviar_email(email_enviado, nome, senha):
    
    send_mail("Envio da senha de usuario", f"Ola {nome} aqui está a sua senha: {senha}", settings.EMAIL_HOST_USER, [f"{email_enviado}"])
   
   