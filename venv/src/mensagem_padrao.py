sensores = {
    'estacao_01': ['sensor_01', 'sensor_02','sensor_03', 'sensor_04', 'sensor_05'],
    'estacao_02': ['sensor_06', 'sensor_07','sensor_08', 'sensor_09', 'sensor_10'],
    'estacao_03': ['sensor_11', 'sensor_12','sensor_13', 'sensor_14', 'sensor_15'],
    'estacao_04': ['sensor_16', 'sensor_17','sensor_18', 'sensor_19', 'sensor_20'],
    'estacao_05': ['sensor_21', 'sensor_22','sensor_23', 'sensor_24', 'sensor_25'],
    'estacao_06': ['sensor_26', 'sensor_27','sensor_28', 'sensor_29', 'sensor_30'],
    'estacao_07': ['sensor_31', 'sensor_32','sensor_33', 'sensor_34', 'sensor_35'],
    'estacao_08': ['sensor_36', 'sensor_37','sensor_38', 'sensor_39', 'sensor_40'],
    'estacao_09': ['sensor_41', 'sensor_42','sensor_43', 'sensor_44', 'sensor_45'],
}

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
    "oxigenio_dissolvido",    #A
    "turbidez",               #B
    "temperatura",            #C
    "condutividade",          #D
    "amonio",                 #E
    "ph"                      #F     
]

periodicidade = "15 minutos"


def criar_mensagem_incricao:
    for i in range(len(estacoes)):
        for j in range(len(parametros_nome)):
            mensagem_padrao = {
                {sensores[i]} : {estacoes[i]},
                "sensors": [
                    {
                        "sensor_id": {sensores[i][j]},
                        "data_type": {parametro[i]},
                        "data_interval": periodicidade
                    }
                ]
            }