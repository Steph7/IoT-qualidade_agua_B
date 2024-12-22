from pymongo import MongoClient

class Estacao:
    def __init__(self, id_estacao, dados):
        self.id_estacao = id_estacao  # ID da estação
        self.dados = dados  # Dicionário com os últimos dados de cada sensor

    def __repr__(self):
        return f"Estacao({self.id_estacao}, {self.dados})"


def obter_ultimo_valor(colecao, sensor):
    # Obter os documentos da coleção, ordenados pela data_hora, e pegar o último (limit(1))
    ultimo_documento = colecao.find().sort("data_hora", -1).limit(1)
    
    # Verificar se há documentos no cursor
    if ultimo_documento.alive:
        documento = ultimo_documento[0]  # O último documento
        # Verifica se o sensor existe no documento
        if sensor in documento:
            return documento[sensor][-1]['valor']  # Retorna o último valor registrado para o sensor
    return None


def obter_dados_estacao(estacao, list_obj):
    # Acessar a coleção da estação
    colecao = db[estacao]
    
    # Inicializa um dicionário para armazenar os dados dos sensores
    dados_estacao = {}
    
    # Lista de sensores que podem ser encontrados na coleção
    sensores = ['amonio', 'temperatura', 'ph', 'oxigenio_dissolvido', 'turbidez', 'condutividade']
    
    # Para cada sensor, obtém o último valor registrado
    for sensor in sensores:
        valor = obter_ultimo_valor(colecao, sensor)
        if valor is not None:
            dados_estacao[sensor] = valor
    
    # Cria um objeto Estacao com os dados coletados
    estacao_obj = Estacao(estacao, dados_estacao)
    
    # Adiciona o objeto à lista
    list_obj.append(estacao_obj)

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['qualidade_agua'] 

    list_obj = []  # Lista para armazenar as instâncias de Estacao

    # Acessar todas as estações no banco de dados
    for estacao in db.list_collection_names():
        obter_dados_estacao(estacao, list_obj)

    # Exibir os dados coletados
    for estacao in list_obj:
        print(estacao)
