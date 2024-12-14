import paho.mqtt.client as mqtt
import json

# Função de callback quando a conexão for realizada
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código {rc}")
    # Subscreve a um tópico
    client.subscribe("topico/teste")

# Função de callback para receber mensagens
def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.payload.decode()}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectando ao broker Mosquitto
client.connect("localhost", 1883, 60)

# Loop principal para receber mensagens
client.loop_start()

# Publicar uma mensagem em um tópico
message = {"dados": "exemplo de mensagem"}
client.publish("topico/teste", json.dumps(message))

