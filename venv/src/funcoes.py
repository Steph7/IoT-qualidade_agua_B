# Lista de parâmetros
parametros_nome = [
    "oxigenio_dissolvido",    #A - 01, 07, 13, 19, 25, 31, 37, 43, 49
    "turbidez",               #B - 02, 08, 14, 20, 26, 32, 38, 44, 50
    "temperatura",            #C - 03, 09, 15, 21, 27, 33, 39, 45, 51
    "condutividade",          #D - 04, 10, 16, 22, 28, 34, 40, 46, 52
    "amonio",                 #E - 05, 11, 17, 23, 29, 35, 41, 47, 53
    "ph"                      #F - 06, 12, 18, 24, 30, 36, 42, 48, 54   
]

 # Os pesos devem estar entre 0 e 1 e a soma dos pesos deve ser 1
    # Os valores foram adpatados da tabela do PNQA https://portalpnqa.ana.gov.br/indicadores-indice-aguas.aspx
    pesos = [
        0.27,   #oxigenio_dissolvido
        0.12,   #turbidez
        0.15,   #temperatura
        0.12,   #condutividade
        0.15,   #amonio
        0.19    #ph
    ]

    # Intervalos em que os parâmetros são bons ou aceitáveis
    limites = {
        "oxigenio_dissolvido": (5, 9),   # Oxigênio Dissolvido entre 5 e 9 mg/L
        "turbidez": (0, 4),              # Turbidez entre 0 e 4 NTU
        "temperatura": (0, 30),          # Temperatura entre 0 e 30 graus
        "condutividade": (70, 750),      # Condutividade entre 70 e 750 mS
        "amonio": (0, 0.5),              # Amônio entre 0 e 0.5 mg/L
        "ph": (6.5, 9.5)                 # pH entre 6.5 e 9.5
    }

# Retornar um valor entre 0 e 100
def normalizar_intervalo(valor, limite_inferior, limite_superior):
    if limite_inferior <= valor <= limite_superior:
        valor_normalizado = 100
    
    elif valor < limite_inferior:
        valor_normalizado = max(0, 100 - (limite_inferior - valor) * 20)
    
    elif valor > limite_superior:
        valor_normalizado = max(0, 100 - (valor - limite_superior) * 20)

    return valor_normalizado 

dados_avaliacao = []

class sensoresEstacao:
    def __init__(self, estacao, parametro, valor, data_hora):
        self.id = id_estacao
        self.o2 = oxigenio_dissolvido
        self.turb = turbidez
        self.temp = temperatura
        self.cond = condutividade
        self.amm = amonio
        self.ph = pH

    def __str__(self):
        return f"Estação: {self.id}, oxigenio_dissolvido: {self.o2}, turbidez: {self.turb}, temperatura: {self.temp}, condutividade: {self.cond}, amonio: {self.amm}, pH: {self.ph}"


def qualificar_agua(dados_avaliacao, pesos, limites):
    parametros = dados_estacao.get(estacao_id, {})

    

# Exemplo de chamada
qualificar_agua("BREPON")
