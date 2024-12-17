import threading
import requests
import time
import paho.mqtt.client as mqtt
import json

# Definir Classe para armazenar os dados coletados
class DadoEstacao:
    def __init__(self, estacao, parametro, valor, data_hora):
        self.estacao = estacao
        self.parametro = parametro
        self.valor = valor
        self.data_hora = data_hora

    def __str__(self):
        return f"Estação: {self.estacao}, Parâmetro: {self.parametro}, Valor: {self.valor} mg/L, Data/Hora: {self.data_hora}"

# Lista de IDs das estações
estacoes = [
    "BREPON",  #01
    "KEWPON",  #02
    "GPRSD8A", #03
    "HAMME2",  #04
    "PUTNEY",  #05
    "CADOG2",  #06
    "BARIERA", #07
    "ERITH1",  #08
    "E03036A"  #09        
]

# Lista de parâmetros
parametros_url = [
    "-do-i-subdaily-mgL",     #A - Oxigênio Dissolvido
    "-turb-i-subdaily-ntu",   #B - Turbidez
    "-temp-i-subdaily-C",     #C - Temperatura
    "-cond-i-subdaily-mS",    #D - Condutividade
    "-amm-i-subdaily-mgL",    #E - Amônio
    "-ph-i-subdaily"          #F - PH     
]

parametros_nome = [
    "oxigenio_dissolvido",    #A
    "turbidez",               #B
    "temperatura",            #C
    "condutividade",          #D
    "amonio",                 #E
    "ph"                      #F     
]

atualizar_nome_param = dict(zip(parametros_url, parametros_nome))

dados_coletados = []

# Coletar dados de cada estação a cada 15 minutos
def coletar_dados_15min(estacao_id, parametro):
    url = f"https://environment.data.gov.uk/hydrology/id/measures/{estacao_id}{parametro}/readings.json?latest"

    try:
        # Fazendo a requisição para a API
        resposta = requests.get(url)
        
        # Verificando o código de status da resposta
        #print(f"Código de Status HTTP para {estacao_id}{parametro}: {resposta.status_code}")
        

        if resposta.status_code == 429:
            retry_after = int(resposta.headers.get("Retry-After", 30))
            time.sleep(retry_after)
            # Tentar novamente após o tempo de espera
            resposta = requests.get(url)

        if resposta.status_code == 200:
            try:
                dados = resposta.json()  # Convertendo a resposta em JSON
                
                # Verificar se a chave 'items' está presente na resposta
                if 'items' in dados:
                    for item in dados['items']:
                        # Extraindo os dados
                        valor = item.get('value')  # Valor da medição
                        data_hora = item.get('dateTime')  # Data e hora

                        if parametro in atualizar_nome_param:
                            parametro = atualizar_nome_param[parametro]

                        dados_coletados.append(DadoEstacao(estacao=estacao_id, parametro=parametro, valor=valor, data_hora=data_hora))
                else:
                    print("Nenhum item de medição encontrado na resposta.")
            
            except ValueError as e:
                print("Erro ao tentar parsear o JSON. Conteúdo da resposta:")
                print(resposta.text) 
        else:
            print(f"Erro na requisição {estacao_id}{parametro} : {resposta.status_code}")
            print(f"Conteúdo da resposta (HTML): {resposta.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")

threads = []

def loop_coletar_dados(client):
    while True:
        for estacao in estacoes:
            for parametro in parametros_url:
                t = threading.Thread(target=coletar_dados_15min, args=(estacao, parametro))
                threads.append(t)
                t.start()
        
        for t in threads:
            t.join();

        for dado in dados_coletados:
            # Estrutura do tópico: 'thames/<estacao>/<parametro>'
            topico = f"thames/{dado.estacao}/{dado.parametro}"

            # Dados a serem enviados
            dados_enviar = {
                "sensor": dado.parametro,
                "valor": dado.valor,
                "data_hora": dado.data_hora
            }

            # Publica a string no tópico
            client.publish(topico, json.dumps(dados_enviar))
            print(f"Mensagem publicada: {topico} - {dados_enviar}")

            #print("\nDados Coletados:")
            #for dado in dados_coletados:
                #print(f"Estação: {dado.estacao}, Parâmetro: {dado.parametro}, Valor: {dado.valor} mg/L, Data/Hora: {dado.data_hora}")
        

            time.sleep(1) # Espera um pouco para não sobrecarregar o broker
        
        
        # Limpar Listas 
        #dados_coletados.clear()
        #threads.clear()

        # Aguarda por novos dados dos sensores
        time.sleep(900)  

        # Loop para manter a conexão ativa até a publicação
        client.loop_forever()
   
# Função de callback para quando o cliente MQTT se conectar
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código {rc}")

# Cria a conexão com o broker
broker = "broker.hivemq.com"
client = mqtt.Client()

# Define o callback de conexão
client.on_connect = on_connect

# Conecta ao broker
client.connect(broker, 1883, 60)

    
loop_coletar_dados(client)
