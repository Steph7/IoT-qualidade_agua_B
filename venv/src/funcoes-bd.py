from pymongo import MongoClient

class Estacao:
    def __init__(self, id_estacao, dados):
        self.id_estacao = id_estacao  # ID da estação
        self.dados = dados  # Dicionário com os últimos dados de cada sensor

    def __repr__(self):
        return f"Estacao({self.id_estacao}, {self.dados})"

# Lista de parâmetros
parametros_nome = [
    "oxigenio_dissolvido",    #A - 01, 07, 13, 19, 25, 31, 37, 43, 49
    "turbidez",               #B - 02, 08, 14, 20, 26, 32, 38, 44, 50
    "temperatura",            #C - 03, 09, 15, 21, 27, 33, 39, 45, 51
    "condutividade",          #D - 04, 10, 16, 22, 28, 34, 40, 46, 52
    "amonio",                 #E - 05, 11, 17, 23, 29, 35, 41, 47, 53
    "ph"                      #F - 06, 12, 18, 24, 30, 36, 42, 48, 54   
]

# Os pesos devem estar entre 0 e 1 e a soma dos pesos deve ser 1
# Os valores foram adpatados da tabela do PNQA https://portalpnqa.ana.gov.br/indicadores-indice-aguas.aspx
pesos = [
    0.27,   #oxigenio_dissolvido
    0.12,   #turbidez
    0.15,   #temperatura
    0.12,   #condutividade
    0.15,   #amonio
    0.19    #ph
]

# Intervalos em que os parâmetros são bons ou aceitáveis
limites = {
    "oxigenio_dissolvido": (5, 9),   # Oxigênio Dissolvido entre 5 e 9 mg/L
    "turbidez": (0, 4),              # Turbidez entre 0 e 4 NTU
    "temperatura": (0, 30),          # Temperatura entre 0 e 30 graus
    "condutividade": (70, 750),      # Condutividade entre 70 e 750 mS
    "amonio": (0, 0.5),              # Amônio entre 0 e 0.5 mg/L
    "ph": (6.5, 9.5)                 # pH entre 6.5 e 9.5
}

 # Retorna o último valor registrado para o sensor
def obter_ultimo_valor(colecao, sensor):
    ultimo_documento = colecao.find().sort("data_hora", -1).limit(1)
    
    if ultimo_documento.alive:
        documento = ultimo_documento[0]  
        if sensor in documento:
            return documento[sensor][-1]['valor']
    return None

# Para cada sensor, obtém o último valor registrado
def obter_dados_estacao(estacao, list_obj):
    colecao = db[estacao]
    dados_estacao = {}
    
    sensores = ['amonio', 'temperatura', 'ph', 'oxigenio_dissolvido', 'turbidez', 'condutividade']
    
    for sensor in sensores:
        valor = obter_ultimo_valor(colecao, sensor)
        if valor is not None:
            dados_estacao[sensor] = valor
    
    estacao_obj = Estacao(estacao, dados_estacao)
    list_obj.append(estacao_obj)

# Retornar um valor entre 0 e 100
def normalizar_intervalo(valor, limite_inferior, limite_superior):
    if limite_inferior <= valor <= limite_superior:
        valor_normalizado = 100
    
    elif valor < limite_inferior:
        valor_normalizado = max(0, 100 - (limite_inferior - valor) * 20)
    
    elif valor > limite_superior:
        valor_normalizado = max(0, 100 - (valor - limite_superior) * 20)

    return valor_normalizado 

# Filtra as notas e pesos válidos (nota > zero)
# Calcula o produtório entre as notas válidas
def calcular_produtorio_com_pesos(notas, pesos):
    notas_validas = [nota for nota in notas if nota > 0]
    pesos_validos = [peso for i, peso in enumerate(pesos) if notas[i] > 0]

    if not notas_validas:
        return 1  # Evita divisão por zero

    soma_pesos_validos = sum(pesos_validos)

    pesos_normalizados = [peso / soma_pesos_validos for peso in pesos_validos]

    produtorio = 1
    for nota, peso_normalizado in zip(notas_validas, pesos_normalizados):
        produtorio *= (nota ** peso_normalizado)

    return produtorio

# Avaliar Qualidade da Água para cada Estação
def nota_qualidade_agua(estacao, pesos, limites):
    notas_estacao = []

    #Avaliar o Oxigênio Dissolvido
    o2 = estacao.get('oxigenio_dissolvido', 0)
    nota_o2 = normalizar_intervalo(o2, limites["oxigenio_dissolvido"][0], limites["oxigenio_dissolvido"][1])
    notas_estacao.append(nota_o2)
    #print(nota_o2)

    #Avaliar a Turbidez
    turb = estacao.get('turbidez', 0)
    nota_turb = normalizar_intervalo(turb, limites["turbidez"][0], limites["turbidez"][1])
    notas_estacao.append(nota_turb)
    #print(nota_turb)

    #Avaliar a Temperatura
    temp = estacao.get('temperatura', 0)
    nota_temp = normalizar_intervalo(temp, limites["temperatura"][0], limites["temperatura"][1])
    notas_estacao.append(nota_temp)
    #print(nota_temp)

    #Avaliar a Condutividade
    cond = estacao.get('condutividade', 0)
    nota_cond = normalizar_intervalo(cond, limites["condutividade"][0], limites["condutividade"][1])
    notas_estacao.append(nota_cond)
    #print(nota_cond)

    #Avaliar a Quantidade de Amônio
    amn = estacao.get('amonio', 0)
    nota_amn = normalizar_intervalo(amn, limites["amonio"][0], limites["amonio"][1])
    notas_estacao.append(nota_amn)
    #print(nota_amn)

    #Avaliar o pH
    ph = estacao.get('ph', 0)
    nota_pH = normalizar_intervalo(ph, limites["ph"][0], limites["ph"][1])
    notas_estacao.append(nota_pH)
    #print(nota_pH)

    produtorio = calcular_produtorio_com_pesos(notas_estacao, pesos)

    return produtorio


def qualificar_agua(produto):
    qualidade = "não qualificado"
    if 0 <= produto <= 25:
        qualidade = "Péssima"

    if 26 <= produto <= 50:
        qualidade = "Ruim"
    
    if 51 <= produto <= 70:
        qualidade = "Razoável"

    if 71 <= produto <= 90:
        qualidade = "Boa"
    
    if 91 <= produto <= 100:
        qualidade = "Ótima"
    
    if produto >= 100:
        qualidade = "Excelente"
    
    return qualidade



if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['qualidade_agua'] 

    lista_estacoes = []  # Lista para armazenar as instâncias de Estacao

    # Acessar todas as estações no banco de dados
    for estacao in db.list_collection_names():
        obter_dados_estacao(estacao, lista_estacoes)

    for estacao in lista_estacoes:
        prod_Teste = nota_qualidade_agua(estacao.dados, pesos, limites)

        estacao = estacao.id_estacao
        colecao = db[estacao] #encontra coleção no BD

        nota_quali = "{:.3f}".format(round(prod_Teste, 3))
        quali = qualificar_agua(prod_Teste)
        
        colecao.update_one(
            {'_id': estacao}, 
            {
                '$push': {'nota': nota_quali, 'qualidade': quali} 
            },
            upsert=True  
        )

        print(estacao)
        print("Nota:", nota_quali, "--- Avaliação:", quali)
        print("\n")