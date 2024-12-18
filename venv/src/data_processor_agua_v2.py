import paho.mqtt.client as mqtt
from pymongo import MongoClient, ASCENDING
import json


# Conecte-se ao MongoDB (no caso, usando o localhost e a porta padrão)
client = MongoClient("mongodb://localhost:27017/")
db = client['qualidade_agua']

# Função de callback para processar os dados recebidos
def on_message(client, userdata, msg):
    try:
        # Recebe a mensagem do broker
        dados = json.loads(msg.payload)

        # Processamento dos dados
        if "sensor" in dados and "valor" in dados:
            estacao = db[dados["estacao"]] #cria coleção no BD
            sensor = estacao[dados["sensor"]] #cria sub-coleção
            sensor.create_index([("data_hora", ASCENDING)], expireAfterSeconds=10800)  #Expira dados após 3 horas
            del dados["estacao"]

        # Processamento dos dados
        if "sensor" in dados and "valor" in dados:
            if dados["sensor"] == "temperatura":
                temperatura_celsius = dados["valor"]
                temperatura_fahrenheit = (temperatura_celsius * 9/5) + 32
                print(f"Temperatura em Fahrenheit: {temperatura_fahrenheit:.2f}°F")
                del dados["sensor"]
                print(json.dumps(dados, indent=4))
                sensor.insert_one(dados) # Inserir dados no BD
            else:
                print("Sensor desconhecido!")
        else:
            # Imprime a mensagem recebida
            print(json.dumps(dados, indent=4))
    
    except json.JSONDecodeError:
        print("Erro ao decodificar a mensagem JSON.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código {rc}")
    # Inscreve no tópico onde a mensagem inicial foi publicada
    client.subscribe("/thames")

# Cria a conexão com o broker
broker = "broker.hivemq.com"
client = mqtt.Client()
client.connect(broker, 1883, 60)

# Inscreve no tópico "dados/coletados"
client.subscribe("/thames/+/temperatura")

# Define a função de callback para mensagens recebidas
client.on_connect = on_connect
client.on_message = on_message

# Loop para escutar novas mensagens
client.loop_forever()
