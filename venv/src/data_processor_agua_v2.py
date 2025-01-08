import paho.mqtt.client as mqtt
from pymongo import MongoClient, ASCENDING
import json


# Conecte-se ao MongoDB (no caso, usando o localhost e a porta padrão)
client = MongoClient("mongodb://mongo:27017/")
db = client['qualidade_agua']

# Função de callback para salvar os dados recebidos
def on_message(client, userdata, msg):
    try:
        # Recebe a mensagem do broker
        dados = json.loads(msg.payload)

        # Salva dados no Banco de Dados
        if "sensor" in dados and "valor" in dados:
            estacao = dados["estacao"]
            sns = dados["sensor"]
            colecao = db[estacao] #cria coleção no BD
            del dados["estacao"]
            del dados["sensor"]
            dados_sns = dados
            
            colecao.update_one(
                {'_id': estacao}, 
                {
                    '$push': {sns: dados_sns} 
                },
                upsert=True  # Cria o documento caso não exista
            )
            print(f"Dados de {sns} da estação {estacao} inseridos no BD com sucesso!")

        else:
            # Imprime a mensagem recebida
            print(json.dumps(dados, indent=4))
    
    except json.JSONDecodeError:
        print("Erro ao decodificar a mensagem JSON.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Função para processar os dados


def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código {rc}")
    # Inscreve no tópico onde a mensagem inicial foi publicada
    client.subscribe("/thames")

# Cria a conexão com o broker
broker = "broker.hivemq.com"
client = mqtt.Client()
client.connect(broker, 1883, 60)

# Inscreve em todos os tópicos
client.subscribe("/thames/#")

# Define a função de callback para mensagens recebidas
client.on_connect = on_connect
client.on_message = on_message

# Loop para escutar novas mensagens
client.loop_forever()
