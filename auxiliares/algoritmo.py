import re
from challenger.models import Transacao
from validadores.validar_algoritmo import verifica_valor_maior_que_100000


def encontrar_arquivos_com_a_mesma_data(arquivos, data):
    
    lista_de_arquivos = []
    for arquivo in arquivo:
        data_arquivo = arquivo.dia_da_transacao.strftime("%Y-%m")
        if data_arquivo == data:
            lista_de_arquivos.append(arquivo)
    
    return lista_de_arquivos

def pegar_transacoes_da_lista(lista_de_arquicos):
    
    lista_transacoes = []
    for arquivo in lista_de_arquicos:
        trasacao = Transacao.objects.filter(arquivo=arquivo).all()
        lista_transacoes.append(trasacao)
    
    return lista_transacoes

def transformar_lista_transacao(transacoes):
    
    lista_transacoes = []
    for x in range(len(transacoes)):
        lista_atual = transacoes[x]
        for i in lista_atual:
            lista_transacoes.append(i)
    return lista_transacoes
    
def transacoes(arquivos ,data):
    
    lista_de_arquicos = encontrar_arquivos_com_a_mesma_data(arquivos, data)
    transacoes = pegar_transacoes_da_lista(lista_de_arquicos)
    lista_transacoes = transformar_lista_transacao(transacoes)
    
    return lista_transacoes

def transacao_suspeita(lista_transacoes):
    
    transacoes_suspeitas = []
    for transacao in lista_transacoes:
        if verifica_valor_maior_que_100000(transacao.valor) == True:
            transacoes_suspeitas.append(transacao)
    return transacao_suspeita

def conta_suspeita(lista_transacoes):
    
    contao = []
    continha = []
    lista_contas_suspeitas = {}
    contas_do_mes = {}
    for transacao in lista_transacoes:
        conta = transacao.numero_banco_emissor
        conta = conta+"Saida"
        if conta not in contas_do_mes:
            contas_do_mes[conta]=0
        conta = transacao.numero_banco_destinatario
        conta = conta+"Entrada"
        if conta not in contas_do_mes:
            contas_do_mes[conta] = 0

    for transacao in lista_transacoes:
        contas_do_mes[transacao.numero_banco_emissor+"Saida"] += transacao.valor_transacao
        contas_do_mes[transacao.numero_banco_destinatario+"Entrada"] += transacao.valor_transacao
        
    for item in contas_do_mes:
        if contas_do_mes[item] >1000000:
            lista_contas_suspeitas[item] = contas_do_mes[item]
    
    contas_suspeitas_entradas = re.findall("\d{3}Entrada", str(lista_contas_suspeitas))
    contas_suspeitas_saidas = re.findall("\d{3}Saida", str(lista_contas_suspeitas))
    
    for conta_entrada in contas_suspeitas_entradas:
        conta = conta_entrada.split("Entrada")
        conta = conta[0]
        transacao = Transacao.objects.filter(numero_banco_destinatario = conta)
        
        continha.append([transacao, lista_contas_suspeitas[conta_entrada], "Entrada"])
    
    for conta_saida in contas_suspeitas_saidas:
        conta = conta_saida.split("Saida")
        conta = conta[0]
        transacao = Transacao.objects.filter(numero_banco_emissor = conta)
        
        contao.append([transacao, lista_contas_suspeitas[conta_saida], "Saida"])
