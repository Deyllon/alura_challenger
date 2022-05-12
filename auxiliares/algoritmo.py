import re
from challenger.models import Transacao
from validadores.validar_algoritmo import verifica_valor_maior_que_100000


def encontrar_arquivos_com_a_mesma_data(arquivos, data):
    
    lista_de_arquivos = []
    for arquivo in arquivos:
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
        if verifica_valor_maior_que_100000(transacao.valor_transacao) == True:
            transacoes_suspeitas.append([transacao.banco_emissor, transacao.agencia_banco_emissor, transacao.numero_banco_emissor,
                                         transacao.banco_destinatario, transacao.agencia_banco_destinatario,
                                         transacao.numero_banco_destinatario, transacao.valor_transacao])
    return transacoes_suspeitas

def cria_dicionario_conta(lista_transacoes):
    
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
    return contas_do_mes
    
def adiciona_valor_as_contas_dicionario(contas_do_mes, lista_transacoes):
    
    for transacao in lista_transacoes:
        contas_do_mes[transacao.numero_banco_emissor+"Saida"] += transacao.valor_transacao
        contas_do_mes[transacao.numero_banco_destinatario+"Entrada"] += transacao.valor_transacao    
    return contas_do_mes

def verifica_e_adiciona_iten_suspeitos(contas_do_mes):
    
    lista_contas_suspeitas = {}
    for item in contas_do_mes:
        if contas_do_mes[item] >1000000:
            lista_contas_suspeitas[item] = contas_do_mes[item]
    return lista_contas_suspeitas

def retorna_suspeitas_entrada(lista_contas_suspeitas):
    
    entrada = re.findall("\d{5}-\d{1}Entrada", str(lista_contas_suspeitas))

    return entrada

def retorna_suspeitas_saidas(lista_contas_suspeitas):
    
    saida = re.findall("\d{5}-\d{1}Saida", str(lista_contas_suspeitas))
    
    return saida
 
def retorna_entradas_suspeitas(contas_suspeitas_entradas, lista_contas_suspeitas):
    
    entrada = []
    for conta_entrada in contas_suspeitas_entradas:
        conta = conta_entrada.split("Entrada")
        conta = conta[0]
        transacao = Transacao.objects.filter(numero_banco_destinatario = conta).first()
        
        banco = transacao.banco_destinatario
        agencia = transacao.agencia_banco_destinatario
        conta = transacao.numero_banco_destinatario
        
        entrada.append([banco, agencia, conta, lista_contas_suspeitas[conta_entrada], "Entrada"])
    return entrada
    
def retorna_saidas_suspeitas(contas_suspeitas_saidas, lista_contas_suspeitas):
    
    saidas = []
    for conta_saida in contas_suspeitas_saidas:
        conta = conta_saida.split("Saida")
        conta = conta[0]
        transacao = Transacao.objects.filter(numero_banco_emissor = conta).first()
        
        banco = transacao.banco_emissor
        agencia = transacao.agencia_banco_emissor
        conta = transacao.numero_banco_emissor
        
        saidas.append([banco, agencia, conta, lista_contas_suspeitas[conta_saida], "Saida"])
    return saidas
    
def conta_suspeita(lista_transacoes):
      
    contas_do_mes = cria_dicionario_conta(lista_transacoes)
    contas_do_mes = adiciona_valor_as_contas_dicionario(contas_do_mes, lista_transacoes)
    lista_contas_suspeitas = verifica_e_adiciona_iten_suspeitos(contas_do_mes)
    
    contas_suspeitas_entradas = retorna_suspeitas_entrada(lista_contas_suspeitas)
    contas_suspeitas_saidas = retorna_suspeitas_saidas(lista_contas_suspeitas)
    
    entradas = retorna_entradas_suspeitas(contas_suspeitas_entradas, lista_contas_suspeitas)
    saidas = retorna_saidas_suspeitas(contas_suspeitas_saidas, lista_contas_suspeitas)

    return entradas, saidas

def contas_saidas(conta_suspeita):
    
    return conta_suspeita[1]

def contas_entradas(conta_suspeita):
    
    return conta_suspeita[0]

def agencias_suspeitas(lista_transacoes):
    
    agencias_do_mes = cria_dicionario_agencia(lista_transacoes)
    agencias_do_mes = adiciona_valor_as_agencias_dicionario(agencias_do_mes, lista_transacoes)
    lista_agencias_suspeitas = verifica_e_adiciona_iten_suspeitos_as_agencias(agencias_do_mes)
    
    agencias_suspeitas_entradas = retorna_agencias_suspeitas_entrada(lista_agencias_suspeitas)
    agencias_suspeitas_saidas = retorna_agencias_suspeitas_saidas(lista_agencias_suspeitas)
    
    entradas = retorna_agencias_entradas_suspeitas(agencias_suspeitas_entradas, lista_agencias_suspeitas)
    saidas = retorna_agencias_saidas_suspeitas(agencias_suspeitas_saidas, lista_agencias_suspeitas)

    return entradas, saidas
    
def cria_dicionario_agencia(lista_transacoes):
    
    agencias_do_mes = {}
    for transacao in lista_transacoes:
        agencia = transacao.agencia_banco_emissor
        agencia = agencia+"Saida"
        if agencia not in agencias_do_mes:
            agencias_do_mes[agencia]=0
        agencia = transacao.agencia_banco_destinatario
        agencia = agencia+"Entrada"
        if agencia not in agencias_do_mes:
            agencias_do_mes[agencia] = 0
    return agencias_do_mes

def adiciona_valor_as_agencias_dicionario(agencias_do_mes, lista_transacoes):
    
    for transacao in lista_transacoes:
        agencias_do_mes[transacao.agencia_banco_emissor+"Saida"] += transacao.valor_transacao
        agencias_do_mes[transacao.agencia_banco_destinatario+"Entrada"] += transacao.valor_transacao    
    return agencias_do_mes

def verifica_e_adiciona_iten_suspeitos_as_agencias(agencias_do_mes):
    
    lista_agencias_suspeitas = {}
    for item in agencias_do_mes:
        if agencias_do_mes[item] >1000000000:
            lista_agencias_suspeitas[item] = agencias_do_mes[item]
    return lista_agencias_suspeitas

def retorna_agencias_suspeitas_entrada(lista_agencias_suspeitas):
    
    entrada = re.findall("\d{4}Entrada", str(lista_agencias_suspeitas))

    return entrada

def retorna_agencias_suspeitas_saidas(lista_agencias_suspeitas):
    
    saida = re.findall("\d{4}Saida", str(lista_agencias_suspeitas))
    
    return saida

def retorna_agencias_entradas_suspeitas(agencias_suspeitas_entradas, lista_agencias_suspeitas):
    entrada = []
    for agencia_entrada in agencias_suspeitas_entradas:
        agencia = agencia_entrada.split("Entrada")
        agencia = agencia[0]
        transacao = Transacao.objects.filter(agencia_banco_destinatario= agencia).first()
        
        banco = transacao.banco_destinatario
        agencia = transacao.agencia_banco_destinatario
        
        entrada.append([banco, agencia, lista_agencias_suspeitas[agencia_entrada], "Entrada"])
    return entrada

def retorna_agencias_saidas_suspeitas(agencias_suspeitas_saidas, lista_agencias_suspeitas):
    
    saidas = []
    for agencia_saida in agencias_suspeitas_saidas:
        agencia = agencia_saida.split("Saida")
        agencia = agencia[0]
        transacao = Transacao.objects.filter(agencia_banco_emissor = agencia).first()
        
        banco = transacao.banco_emissor
        agencia = transacao.agencia_banco_emissor
        
        saidas.append([banco, agencia, lista_agencias_suspeitas[agencia_saida], "Saida"])
    return saidas

def agencias_saidas(agencia_suspeita):
    
    return agencia_suspeita[1]

def agencias_entradas(agencia_suspeita):
    
    return agencia_suspeita[0]