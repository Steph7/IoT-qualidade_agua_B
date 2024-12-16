import paho.mqtt.client as mqtt
import json

# Função de callback para quando a conexão com o broker for estabelecida
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com o código {rc}")
    
    # Dados coletados (exemplo de temperatura)
    dados = {"sensor": "temperatura", "valor": 23.5}
    
    # Publica os dados no tópico "dados/coletados"
    client.publish("dados/coletados", json.dumps(dados))
    print("Dados publicados.")

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
