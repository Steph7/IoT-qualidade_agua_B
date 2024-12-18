# Processamento dos dados

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
parametros_nome = [
    "oxigenio_dissolvido",    #A - 01, 07, 13, 19, 25, 31, 37, 43, 49
    "turbidez",               #B - 02, 08, 14, 20, 26, 32, 38, 44, 50
    "temperatura",            #C - 03, 09, 15, 21, 27, 33, 39, 45, 51
    "condutividade",          #D - 04, 10, 16, 22, 28, 34, 40, 46, 52
    "amonio",                 #E - 05, 11, 17, 23, 29, 35, 41, 47, 53
    "ph"                      #F - 06, 12, 18, 24, 30, 36, 42, 48, 54   
]

dados_enviar = {
                #"sensor": dado.parametro,
                "data_hora": dado.data_hora,
                "valor": dado.valor
            }

class sensoresEstacao:
    def __init__(self, id_estacao, oxigenio_dissolvido, turbidez, temperatura, condutividade, amonio, pH):
        self.id = id_estacao
        self.o2 = oxigenio_dissolvido
        self.turb = turbidez
        self.temp = temperatura
        self.cond = condutividade
        self.amn = amonio
        self.ph = pH

    def __str__(self):
        return f"Estação: {self.id}, oxigenio_dissolvido: {self.o2}, turbidez: {self.turb}, temperatura: {self.temp}, condutividade: {self.cond}, amonio: {self.amn}, pH: {self.ph}"


dados_coletados = []

for i in estacoes:
    for j in parametros_nome:
        if "estacao" in dados:
            if dados["estacao"] == estacoes[i]:
                dados_coletados.append(sensoresEstacao(estacoes[i], )
                temperatura_celsius = dados["valor"]
                temperatura_fahrenheit = (temperatura_celsius * 9/5) + 32
                print(f"Temperatura em Fahrenheit: {temperatura_fahrenheit:.2f}°F")
            else:
                print("Sensor desconhecido!")
        else:
            # Imprime a mensagem recebida
            print(json.dumps(dados, indent=4))