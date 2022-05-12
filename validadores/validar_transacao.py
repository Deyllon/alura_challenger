from  challenger.models import Transacao
from xml.etree import ElementTree


def verificar_se_data_da_transacao_ja_adicionada(data_primeira_linha):
    
    transacao = Transacao.objects.filter(dia_da_transacao = data_primeira_linha).first()
    return transacao
    
def verifica_se_e_vazio(transacoes):
    
    if transacoes != None:
        return True
    
    return False

def verifica_se_tem_item_vazio(transacao):
    
    if "" in transacao:
        return True
    
    return False

def verifica_se_arquivo_esta_vazio(arquivo):
    
    if arquivo is None:
        return True
    
    return False
