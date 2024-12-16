import time
from pymongo import MongoClient
import socket

# Configurações do Graphite (ajuste conforme necessário)
GRAPHITE_HOST = '127.0.0.1'
GRAPHITE_PORT = 2003

# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['meu_banco']
collection = db['minha_colecao']

# Função para enviar dados para o Graphite
def send_to_graphite(metric_name, value, timestamp):
    message = f"{metric_name} {value} {timestamp}\n"
    sock = socket.socket()
    sock.connect((GRAPHITE_HOST, GRAPHITE_PORT))
    sock.sendall(message.encode())
    sock.close()

# Buscar os dados no MongoDB
for doc in collection.find():
    sensor = doc['sensor']
    value = doc['valor']
    timestamp = int(time.mktime(time.strptime(doc['timestamp'], "%Y-%m-%dT%H:%M:%S")))
    
    # Enviar os dados para o Graphite
    send_to_graphite(f"agua.{sensor}", value, timestamp)

# Fechar a conexão com o MongoDB
client.close()
