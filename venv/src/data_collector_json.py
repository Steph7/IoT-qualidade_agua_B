import paho.mqtt.client as mqtt
import json

# Função de callback para quando a conexão com o broker for estabelecida
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com o código {rc}")
    
    # Dados coletados (exemplo de temperatura)
    dados_t = {"sensor": "temperatura", "valor": 23.5}
    dados_u = {"sensor": "umidade", "valor": 65.9}
    dados_p = {"sensor": "pressão", "valor": 15}

    # Publica os dados no tópico "dados/coletados"
    client.publish("dados/temperatura", json.dumps(dados_t))
    print("Dados publicados Temperatura. \n")

    client.publish("dados/umidade", json.dumps(dados_u))
    print("Dados publicados Umidade. \n")

    client.publish("dados/pressao", json.dumps(dados_p))
    print("Dados publicados Pressão. \n")

    # Desconectar após a publicação
    client.disconnect()

# Cria a conexão com o broker
broker = "broker.hivemq.com"
client = mqtt.Client()

# Define o callback de conexão
client.on_connect = on_connect

# Conecta ao broker
client.connect(broker, 1883, 60)

# Loop para manter a conexão ativa até a publicação
client.loop_forever()
