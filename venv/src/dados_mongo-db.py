from pymongo import MongoClient, ASCENDING
import json

# Conecta ao MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Selecionar o banco de dados 'qualidade_agua'
db = client.qualidade_agua

# Acessar várias coleções
colecao_estacao_01 = db.estacao_01
colecao_estacao_02 = db.estacao_02
colecao_estacao_03 = db.estacao_03

"""
# Criar 9 coleções para as estações
for estacao_num in range(1, 10):
    estacao_nome = f"estacao_0{estacao_num}"
    
    # Criar coleção para a estação
    estacao = db[estacao_nome]
    
    # Criar 6 subcoleções para os sensore"
    for sensor_num in range(1, 7):
        sensor_nome = f"sensor_0{sensor_num}"
        sensor_data = estacao[sensor_nome]
        
        # Criar um índice TTL (Time To Live) na coleção para o campo 'timestamp'
        sensor_data.create_index([("timestamp", ASCENDING)], expireAfterSeconds=10800)  # Expira após 3 horas
"""
# Listar todos os bancos de dados
bancos_de_dados = client.list_database_names()
print("Bancos de dados:", bancos_de_dados)