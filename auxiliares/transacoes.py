import datetime
import re
from challenger.models import Transacao
from validadores.validar_transacao import verifica_se_e_vazio, verifica_se_tem_item_vazio, verificar_se_data_da_transacao_ja_adicionada



def pegar_linhas_arquivos(arquivo):
    return [x.decode('utf8').strip() for x in arquivo.readlines()]

def pegar_transacoes():
    if Transacao.objects.exists():
        transacoes = Transacao.objects.all()
    
        return transacoes
    
    return None

def formatar_horarios(transacoes):
    
    import_data= []
    
    for item in transacoes:
        horario = item.horario_import.strftime("%Y/%m/%d - %H:%M:%S")
        import_data.append(horario)
    
    return import_data

def formatar_data(transacoes):
    import_data= []
    
    for item in transacoes:
        horario = item.dia_da_transacao.strftime("%Y/%m/%d")
        import_data.append(horario)
    
    return import_data

def pegar_data_primeira_linha(linhas):
    
    primeira_linha = linhas[0]
    data_primeira_linha = pegar_data(primeira_linha)
    
    return data_primeira_linha
    

def pegar_data(primeira_linha):
    
    return re.findall(r"\d{4}\-\d{2}\-\d{2}", primeira_linha)[0]

def pegar_data_transacao(dia_da_transacao):
    
    return dia_da_transacao.strip(" ")

def salvar_transacao(linhas, data_primeira_linha, request):
    
    for linha in linhas:
        transacao = linha.split(",")
        
        if verifica_se_tem_item_vazio(transacao):
            return
        
        
        banco_emissor = transacao[0]
        agencia_banco_emissor = transacao[1] 
        numero_banco_emissor = transacao[2]
        banco_destinatario = transacao[3]
        agencia_banco_destinatario = transacao[4]
        numero_banco_destinatario = transacao[5]
        valor_transacao = transacao[6]
        dia_da_transacao = transacao[7]
        
        data = pegar_data_transacao(dia_da_transacao)
        
        if data[0:10] == data_primeira_linha:    
            transacao = Transacao.objects.create(banco_emissor= banco_emissor, agencia_banco_emissor= agencia_banco_emissor,
                                                 numero_banco_emissor= numero_banco_emissor, banco_destinatario= banco_destinatario,
                                                 agencia_banco_destinatario= agencia_banco_destinatario,
                                                 numero_banco_destinatario= numero_banco_destinatario, valor_transacao= valor_transacao,
                                                 dia_da_transacao= data[0:10])
            
            transacao.save()
            
def ler_arquivo_e_salvar_transacao(arquivo,request):
    
    linhas = pegar_linhas_arquivos(arquivo)
    data_primeira_linha = pegar_data_primeira_linha(linhas)
    db_transacoes = verificar_se_data_da_transacao_ja_adicionada(data_primeira_linha)
    
    if verifica_se_e_vazio(db_transacoes):
        return
    
    salvar_transacao(linhas, data_primeira_linha,request)