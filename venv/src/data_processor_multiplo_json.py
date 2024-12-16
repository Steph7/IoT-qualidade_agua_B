import paho.mqtt.client as mqtt
import json

# Função para processar dados de temperatura
def processar_temperatura(dados):
    try:
        temperatura = dados["valor"]  # Assumindo que o JSON tem um campo 'valor'
        temperatura_fahrenheit = (temperatura * 9/5) + 32
        print(f"Temperatura em Fahrenheit: {temperatura_fahrenheit:.2f}°F")
    except KeyError:
        print("Erro: Dados de temperatura não encontrados!")
    except ValueError:
        print("Erro ao processar o valor da temperatura!")

# Função para processar dados de umidade
def processar_umidade(dados):
    try:
        umidade = dados["valor"]  # Assumindo que o JSON tem um campo 'valor'
        print(f"Umidade: {umidade}%")
    except KeyError:
        print("Erro: Dados de umidade não encontrados!")
    except ValueError:
        print("Erro ao processar o valor da umidade!")

# Função para processar dados de pressão
def processar_pressao(dados):
    try:
        pressao = dados["valor"]  # Assumindo que o JSON tem um campo 'valor'
        print(f"Pressão: {pressao} hPa")
    except KeyError:
        print("Erro: Dados de pressão não encontrados!")
    except ValueError:
        print("Erro ao processar o valor da pressão!")

# Função de callback para processar dados conforme o tópico
def on_message(client, userdata, msg):
    try:
        # Decodifica a mensagem para JSON
        dados = json.loads(msg.payload.decode())
        print(f"Mensagem recebida no tópico {msg.topic}: {dados}")

        # Checa o tópico e chama a função apropriada
        if msg.topic == "dados/temperatura":
            processar_temperatura(dados)
        elif msg.topic == "dados/umidade":
            processar_umidade(dados)
        elif msg.topic == "dados/pressao":
            processar_pressao(dados)
        else:
            print("Tópico desconhecido!")

    except json.JSONDecodeError:
        print(f"Erro ao decodificar a mensagem JSON no tópico {msg.topic}.")
    except Exception as e:
        print(f"Ocorreu um erro ao processar a mensagem: {e}")

# Cria a conexão com o broker
broker = "broker.hivemq.com"
client = mqtt.Client()

# Define a função de callback para mensagens recebidas
client.on_message = on_message

# Conecta ao broker
client.connect(broker, 1883, 60)

# Inscreve nos tópicos que deseja processar
client.subscribe("dados/temperatura")
client.subscribe("dados/umidade")
client.subscribe("dados/pressao")

# Loop para escutar novas mensagens
client.loop_forever()
