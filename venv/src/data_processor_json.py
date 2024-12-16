import paho.mqtt.client as mqtt
import json

# Função de callback para processar os dados recebidos
def on_message(client, userdata, msg):
    try:
        # Recebe a mensagem do broker
        dados = json.loads(msg.payload)
        print(f"Dados recebidos: {dados}")
        
        # Processamento dos dados (exemplo: conversão de temperatura)
        if "sensor" in dados and "valor" in dados:
            if dados["sensor"] == "temperatura":
                temperatura_celsius = dados["valor"]
                temperatura_fahrenheit = (temperatura_celsius * 9/5) + 32
                print(f"Temperatura em Fahrenheit: {temperatura_fahrenheit:.2f}°F")
            else:
                print("Sensor desconhecido!")
        else:
            print("Dados incompletos ou inválidos!")
    
    except json.JSONDecodeError:
        print("Erro ao decodificar a mensagem JSON.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Cria a conexão com o broker
broker = "broker.hivemq.com"
client = mqtt.Client()
client.connect(broker, 1883, 60)

# Inscreve no tópico "dados/coletados"
client.subscribe("dados/coletados")

# Define a função de callback para mensagens recebidas
client.on_message = on_message

# Loop para escutar novas mensagens
client.loop_forever()
