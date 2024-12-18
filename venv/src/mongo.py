from pymongo import MongoClient

# Conecte-se ao MongoDB (no caso, usando o localhost e a porta padrão)
client = MongoClient("mongodb://localhost:27017/")

# Listar todos os bancos de dados
bancos_de_dados = client.list_database_names()
print("Bancos de dados:", bancos_de_dados)

db = client['qualidade_agua']

# CONFIGURAÇAO MONGO


# Para cada banco de dados, listar suas coleções
for db_name in bancos_de_dados:
    db = client[db_name]
    colecoes = db.list_collection_names()
    print(f"\nColeções no banco de dados '{db_name}': {colecoes}")
"""   "
    for c in colecoes:
        print(f"\nSub-coleções '{c}'")
        subs = db[c]
    
    docs = subs.find()
    for doc in docs:
            print(doc)


# Selecionar o banco de dados e a coleção
db = client['IoT_qualidade_agua']  # Seleciona o banco de dados
colecao = db['estacao_04']  # Seleciona a coleção

# Deletar todos os documentos da coleção
colecao.delete_many({})

colecao.drop()


client.drop_database('IoT_qualidade_agua')
"""