import json

sensores = [
    ('estacao_01', ['sensor_01', 'sensor_02','sensor_03', 'sensor_04', 'sensor_05', 'sensor_06']),
    ('estacao_02', ['sensor_07','sensor_08', 'sensor_09', 'sensor_10', 'sensor_11', 'sensor_12']),
    ('estacao_03', ['sensor_13','sensor_14', 'sensor_15', 'sensor_16', 'sensor_17', 'sensor_18']),
    ('estacao_04', ['sensor_19','sensor_20', 'sensor_21', 'sensor_22', 'sensor_23', 'sensor_24']),
    ('estacao_05', ['sensor_25','sensor_26', 'sensor_27', 'sensor_28', 'sensor_19', 'sensor_30']),
    ('estacao_06', ['sensor_31','sensor_32', 'sensor_33', 'sensor_34', 'sensor_35', 'sensor_36']),
    ('estacao_07', ['sensor_37','sensor_38', 'sensor_39', 'sensor_40', 'sensor_41', 'sensor_42']),
    ('estacao_08', ['sensor_43','sensor_44', 'sensor_45', 'sensor_46', 'sensor_47', 'sensor_48']),
    ('estacao_09', ['sensor_49','sensor_50', 'sensor_51', 'sensor_52', 'sensor_53', 'sensor_54'])
]

estacoes = [
    "BREPON",  #01
    "KEWPON",  #02
    "GPRSD8A", #03
    "HAMME2",  #04
    "PUTNEY",  #05
    "CADOG2",  #06
    "BARIERA", #07
    "ERITH1",  #08
    "E03036A"  #09        
]

# Lista de parâmetros
parametros_nome = [
    "oxigenio_dissolvido",    #A - 01, 07, 13, 19, 25, 31, 37, 43, 49
    "turbidez",               #B - 02, 08, 14, 20, 26, 32, 38, 44, 50
    "temperatura",            #C - 03, 09, 15, 21, 27, 33, 39, 45, 51
    "condutividade",          #D - 04, 10, 16, 22, 28, 34, 40, 46, 52
    "amonio",                 #E - 05, 11, 17, 23, 29, 35, 41, 47, 53
    "ph"                      #F - 06, 12, 18, 24, 30, 36, 42, 48, 54   
]

periodicidade = "15 minutos"

mensagem_completa = []

def criar_mensagem_incricao():    
    for i in range(len(estacoes)):
        sensores_por_estacao = []
        for j in range(len(parametros_nome)):
            sns = {
                    "sensor_id": f"{sensores[i][1][j]}",
                    "data_type": f"{parametros_nome[j]}",
                    "data_interval": periodicidade
                }
            sensores_por_estacao.append(sns)
            
        mensagem_padrao = {
            f"{sensores[i][0]}": f"{estacoes[i]}", 
            "sensors" : sensores_por_estacao
        }           
        mensagem_completa.append(mensagem_padrao)
    return mensagem_completa

# Exibindo as mensagens
criar_mensagem_incricao()
for msg in mensagem_completa:
    print(json.dumps(msg, indent=4))