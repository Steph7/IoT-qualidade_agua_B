from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['novo_banco_de_dados']
db.test_collection.insert_one({"mensagem": "teste"})
print("Banco de dados e coleção criados com sucesso!")