from auxiliares.usuarios import gerar_senha, pegar_usuario, pegar_usuarios, salvar_usuario
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from validadores.validar_usuario import validar_email, verifica_se_email_ja_existe
from django.contrib import auth


def cadastro(request):
    
    if request.method == "POST":
        
        nome = request.POST["nome"]
        email = request.POST["email"]
        if not validar_email(email):
            return redirect("cadastro")
        
        if verifica_se_email_ja_existe(email):
            return redirect("cadastro")
        
        senha = gerar_senha()
        
        
        salvar_usuario(nome, email, senha)
        
        return redirect("login")
    
    return render(request, "cadastro.html")

def login(request):
    
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]

        username = User.objects.filter(email= email).values_list('username', flat=True).get()
        
        login = auth.authenticate(request, username= username, password=senha)
        
        auth.login(request, login)
        
        return redirect('usuarios_cadastrados')
        
    return render(request, "login.html")

def usuarios_cadastrados(request):
    
        
    usuario = pegar_usuarios(request)
        
    contexto = {
        "usuarios" : usuario
    }
          
    return render(request, "usuarios_cadastrados.html", contexto)

def editar_usuario(request, pk):
    
    usuario = pegar_usuario(pk)
    
    contexto = {
        "usuario": usuario
    }
    
    if request.method == "POST":
        nome = request.POST["nome"]
        email = request.POST["email"]
        senha = request.POST["senha"]
             
        editar_usuario(pk, nome, email, senha)
        
        return redirect("usuarios_cadastrados")
    
    return render(request, "editar_usuario.html", contexto)

def logout(request):
    
    auth.logout(request)
    return redirect('index')
