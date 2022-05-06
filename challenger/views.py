from django.shortcuts import redirect, render
from auxiliares.transacoes import formatar_data, ler_arquivo_e_salvar_transacao, pegar_transacoes, formatar_horarios
from validadores.validar_transacao import verifica_se_arquivo_esta_vazio


def index(request):
    
    if request.user.is_authenticated:
    
        transacoes = pegar_transacoes() 
        
        if transacoes != None:
            horarios = formatar_horarios(transacoes)
            transacoes = formatar_data(transacoes)
        
            contexto = {
                'transacoes': transacoes,
                'horarios': horarios
            }   
        
            if request.method == "POST":
            
                arquivo = request.FILES['file']
            
                if verifica_se_arquivo_esta_vazio(arquivo):
                    return redirect("index")
            
                ler_arquivo_e_salvar_transacao(arquivo,request)
            
                return redirect("index")
    
            return render(request,"form.html", contexto)
        return render(request,"form.html")
    
    return redirect("login")

