import json
import paho.mqtt.client as mqtt

# Função de callback para quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.payload.decode()}")
    
    # Carregar dados antigos
    dados = carregar_dados()
    
    # Atualizar com os novos dados
    dados["mensagem"] = msg.payload.decode()
    
    # Salvar novamente no arquivo JSON
    salvar_dados(dados)

# Função de callback para quando a conexão for bem-sucedida
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código {rc}")
    client.subscribe("topico/teste")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Loop para receber mensagens
client.loop_start()
