from pymongo import MongoClient
from datetime import datetime

# Definindo a classe para armazenar os dados da estação
class sensoresEstacao:
    def __init__(self, id_estacao, oxigenio_dissolvido, turbidez, temperatura, condutividade, amonio, pH):
        self.id = id_estacao
        self.o2 = oxigenio_dissolvido
        self.turb = turbidez
        self.temp = temperatura
        self.cond = condutividade
        self.amn = amonio
        self.ph = pH

    def __str__(self):
        return f"Estação: {self.id}, oxigenio_dissolvido: {self.o2}, turbidez: {self.turb}, temperatura: {self.temp}, condutividade: {self.cond}, amonio: {self.amn}, pH: {self.ph}"

# Função para obter o último valor de uma subcoleção
def obter_ultimo_valor(colecao, subcolecao):
    # Ordena os documentos pela data_hora e pega o último (limit(1))
    ultimo_documento = colecao[subcolecao].find().sort('data_hora', -1).limit(1)
    documento = next(ultimo_documento, None)
    if documento:
        return documento['valor']
    else:
        return None

# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['qualidade_agua']

# Função para consultar os dados mais recentes de uma estação
def obter_dados_estacao(estacao, list_obj):
    colecao = db[estacao]

    # Obter o último valor de cada subcoleção
    o2 = obter_ultimo_valor(colecao, 'oxigenio_dissolvido')
    turb = obter_ultimo_valor(colecao, 'turbidez') 
    temp = obter_ultimo_valor(colecao, 'temperatura')
    cond = obter_ultimo_valor(colecao, 'condutividade') 
    amn = obter_ultimo_valor(colecao, 'amonio')
    ph = obter_ultimo_valor(colecao, 'ph') 

    # Criar o objeto Estacao com os dados coletados
    estacao_obj = sensoresEstacao(estacao, o2, turb, temp, cond, amn, ph)

    # Adicionar o objeto Estacao na lista
    list_obj.append(estacao_obj)

# Lista para armazenar os objetos Estacao
list_obj = []

# Percorrer todas as coleções (estações) do banco de dados 'qualidade_agua'
for estacao in db.list_collection_names():
    # Adicionar os dados de cada estação na lista
    obter_dados_estacao(estacao, list_obj)

# Exibir os objetos de todas as estações
for estacao in list_obj:
    print(estacao)

# Fechar a conexão com o MongoDB
client.close()
