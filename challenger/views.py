from django.shortcuts import redirect, render
from auxiliares.transacoes import formatar_data, formatar_data_do_arquivo, formatar_horario_do_arquivo, ler_arquivo_e_salvar_transacao, pegar_arquivo, pegar_detalhe_arquivo, pegar_transacoes, formatar_horarios
from challenger.models import Arquivo
from validadores.validar_transacao import verifica_se_arquivo_esta_vazio


def index(request):
    
    if request.user.is_authenticated:
    
        arquivos = pegar_arquivo() 
        if request.method == "POST":
            
            arquivo = request.FILES['file']
                
            if verifica_se_arquivo_esta_vazio(arquivo):
                return redirect("index")
                    
            ler_arquivo_e_salvar_transacao(arquivo,request)
                
            return redirect("index")
        
        if arquivos != None:
            horarios = formatar_horarios(arquivos)
            datas_transacoes = formatar_data(arquivos)
        
            contexto = {
                'arquivos': arquivos,
                'horarios': horarios,
                'datas_transacoes': datas_transacoes
            }   
            
            return render(request,"form.html", contexto)
        
        return render(request,"form.html")
    
    return redirect("login")

def detalhes(request, pk):
    
    arquivo = pegar_detalhe_arquivo(pk)
    
    transacoes = pegar_transacoes(arquivo)
    horario = formatar_horario_do_arquivo(arquivo)
    data = formatar_data_do_arquivo(arquivo)
    
    contexto = {
        "transacoes": transacoes,
        "arquivo": arquivo,
        "horario": horario,
        "data": data
    }
    
    return render(request, "detalhes.html", contexto)

def transacoes_suspeitas(request):
    if request.method == "POST":
        data = request.POST["data"]
        arquivos = Arquivo.objects.all()
        print(data)
        print(type(data))
        arquivo = Arquivo.objects.first()
        print(arquivo.dia_da_transacao)
        print(type(arquivo.dia_da_transacao))
        
        return redirect("index")
    return render(request, "transacoes_suspeitas.html")