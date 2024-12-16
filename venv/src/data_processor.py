import paho.mqtt.client as mqtt

# Função de callback para processar os dados recebidos
def on_message(client, userdata, msg):
    # Recebe a mensagem do broker como string
    dados = msg.payload.decode()  # Decodifica para string

    # Processamento da string (exemplo: extraindo a temperatura)
    print(f"Dados recebidos: {dados}")
    
    # Verifica se a string contém a palavra 'Temperatura'
    if "Temperatura" in dados:
        try:
            # Extrai o valor da temperatura
            temperatura = float(dados.split(":")[1].strip().replace("°C", ""))
            temperatura_fahrenheit = (temperatura * 9/5) + 32
            print(f"Temperatura em Fahrenheit: {temperatura_fahrenheit:.2f}°F")
        except ValueError:
            print("Erro ao processar a temperatura!")
    else:
        print("Dados não reconhecidos.")

# Cria a conexão com o broker
broker = "broker.hivemq.com"
client = mqtt.Client()

# Define a função de callback para mensagens recebidas
client.on_message = on_message

# Conecta ao broker
client.connect(broker, 1883, 60)

# Inscreve no tópico "dados/coletados"
client.subscribe("dados/coletados")

# Loop para escutar novas mensagens
client.loop_forever()
