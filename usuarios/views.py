from auxiliares.usuarios import editar_usuarios, enviar_email, gerar_senha, pegar_usuario, pegar_usuarios, salvar_usuario
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from usuarios.models import Usuarios
from validadores.validar_usuario import validar_email, verifica_se_email_ja_existe
from django.contrib import auth, messages



def cadastro(request):
    
    if request.method == "POST":
        
        nome = request.POST["nome"]
        email = request.POST["email"]
        if not validar_email(email):
            
            messages.error(request," Email não é valido")
            return redirect("cadastro")
        
        if verifica_se_email_ja_existe(email):
            
            messages.error(request," Email já cadastrado")
            return redirect("cadastro")
        
        senha = gerar_senha()
        
        enviar_email(email, nome, senha)
        
        salvar_usuario(nome, email, senha)
        print(senha)
        
        messages.success(request,"Senha enviada no email")
        return redirect("login")
    
    return render(request, "cadastro.html")

def login(request):
    
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
        if not User.objects.filter(email=email).exists():
            messages.error(request," Email não existe")
            return redirect ("login")
        usuario = get_object_or_404(Usuarios, email=email)
        
        if usuario.desativado == True:
            
            messages.error(request," Usuario desativado")
            return redirect ("login")
        username = User.objects.filter(email= email).values_list('username', flat=True).get()
        
        login = auth.authenticate(request, username= username, password=senha)
        
        if login is None:
            messages.error(request, "Email ou senha errada")
            return redirect ("login")
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
        nome = request.POST["nome_usuario"]
        email = request.POST["email_usuario"]
             
        editar_usuarios(pk, nome, email)
        
        return redirect("usuarios_cadastrados")
    
    return render(request, "editar_usuario.html", contexto)

def logout(request):
    
    auth.logout(request)
    return redirect('index')

def deletar(request, email):
    
    usuario = get_object_or_404(Usuarios, email= email)
    
    
    usuario.desativado = True
        
    usuario.save(update_fields=["desativado"])
        
    return redirect("usuarios_cadastrados")
         