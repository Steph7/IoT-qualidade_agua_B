from pymongo import MongoClient

# Conectando ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['qualidade_agua']

# Acessar a coleção da estação, por exemplo, GPRSD8A
estacao = db['GPRSD8A']

# Buscar um documento qualquer da estação (usaremos o primeiro documento encontrado)
documento = estacao.find_one()

# Exibir os campos do documento
if documento:
    print("Campos na estação GPRSD8A (sensores):")
    for campo in documento:
        print(campo)
else:
    print("Nenhum documento encontrado.")
