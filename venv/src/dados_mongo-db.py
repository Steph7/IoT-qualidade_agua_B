from pymongo import MongoClient
import json

# Conecta ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.mydatabase
collection = db.mycollection

# Dados JSON
dados = {
    "sensor": "temperatura",
    "valor": 23.5
}

# Salva o JSON diretamente (o MongoDB converte para BSON)
collection.insert_one(dados)

# Recupera o JSON armazenado
resultado = collection.find_one({"sensor": "temperatura"})
print(resultado)  # O MongoDB devolve o dado como JSON
