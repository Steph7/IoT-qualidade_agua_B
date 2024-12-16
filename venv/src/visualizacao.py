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
    try:
        message = f"{metric_name} {value} {timestamp}\n"
        sock = socket.socket()
        sock.connect((GRAPHITE_HOST, GRAPHITE_PORT))
        sock.sendall(message.encode())
        sock.close()
        print(f"Dados enviados para o Graphite: {metric_name} {value} {timestamp}")
    except Exception as e:
        print(f"Erro ao enviar para o Graphite: {e}")

# Buscar os dados no MongoDB
for doc in collection.find():
    # Verifique se os dados estão no formato esperado
    if 'sensor' in doc and 'valor' in doc and 'timestamp' in doc:
        sensor = doc['sensor']
        value = doc['valor']
        
        # Converter o timestamp para um valor numérico (timestamp Unix)
        try:
            timestamp = int(time.mktime(time.strptime(doc['timestamp'], "%Y-%m-%dT%H:%M:%S")))
        except ValueError as e:
            print(f"Erro ao converter o timestamp: {e} para o documento {doc}")
            continue  # Pula para o próximo documento

        # Enviar os dados para o Graphite
        send_to_graphite(f"agua.{sensor}", value, timestamp)
    else:
        print(f"Documento sem os campos esperados: {doc}")

# Fechar a conexão com o MongoDB
client.close()
