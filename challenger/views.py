from django.http import JsonResponse
from django.shortcuts import redirect, render
from auxiliares.algoritmo import agencias_entradas, agencias_saidas, agencias_suspeitas, conta_suspeita, contas_entradas, contas_saidas, transacao_suspeita, transacoes
from auxiliares.transacoes import formatar_data, formatar_data_do_arquivo, formatar_horario_do_arquivo, ler_arquivo_e_salvar_transacao, pegar_arquivo, pegar_detalhe_arquivo, pegar_transacoes, formatar_horarios
from challenger.models import Arquivo
from validadores.validar_transacao import  verifica_se_arquivo_esta_vazio


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
        else:
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
    
    return render(request, "transacoes_suspeitas.html")

def recebe_e_devolve_transacoes(request):
    
    data = request.POST.get("arquivo")
        
    arquivos = Arquivo.objects.all()
        
    lista_transacoes = transacoes(arquivos ,data)
        
    transacoes_suspeitas = transacao_suspeita(lista_transacoes)
    
    contas_entrada_e_saidas = conta_suspeita(lista_transacoes)
        
    contas_saida_suspeitas = contas_saidas(contas_entrada_e_saidas)
    contas_entrada_suspeitas = contas_entradas(contas_entrada_e_saidas)
        
    agencias_entrada_e_saida = agencias_suspeitas(lista_transacoes)
        
    agencias_saida_suspeitas = agencias_saidas(agencias_entrada_e_saida)
    agencias_entrada_suspeitas = agencias_entradas(agencias_entrada_e_saida)
        
    return JsonResponse({"transacoes_suspeitas": transacoes_suspeitas, "contas_saida": contas_saida_suspeitas, "contas_entrada": contas_entrada_suspeitas,
                         "agencias_saida": agencias_saida_suspeitas, "agencias_entrada": agencias_entrada_suspeitas})
