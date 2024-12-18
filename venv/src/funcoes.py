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


def nota_qualidade_agua(dados_avaliacao, pesos, limites):
    #Avaliar o Oxigênio Dissolvido
    nota_o2 = normalizar_intervalo(dados_avaliacao.o2, limites["oxigenio_dissolvido"][0], limites["oxigenio_dissolvido"][1])
    nota_o2_pond = nota_o2**pesos[0]

    #Avaliar a Turbidez
    nota_turb = normalizar_intervalo(dados_avaliacao.turb, limites["turbidez"][0], limites["turbidez"][1])
    nota_turb_pond = nota_turb**pesos[1]

    #Avaliar a Temperatura
    nota_temp = normalizar_intervalo(dados_avaliacao.temp, limites["temperatura"][0], limites["temperatura"][1])
    nota_temp_pond = nota_temp**pesos[2]

    #Avaliar a Condutividade
    nota_cond = normalizar_intervalo(dados_avaliacao.cond, limites["condutividade"][0], limites["condutividade"][1])
    nota_cond_pond = nota_cond**pesos[3]

    #Avaliar a Quantidade de Amônio
    nota_amn = normalizar_intervalo(dados_avaliacao.amn, limites["amonio"][0], limites["amonio"][1])
    nota_amn_pond = nota_amn**pesos[4]

    #Avaliar o pH
    nota_pH = normalizar_intervalo(dados_avaliacao.ph, limites["ph"][0], limites["ph"][1])
    nota_pH_pond = nota_pH**pesos[5]

    produtorio = nota_o2_pond * nota_turb_pond * nota_temp_pond * nota_cond_pond * nota_amn_pond * nota_pH_pond

    return produtorio


def qualificar_agua(produto):
    if 0 <= produto <= 25:
        qualidade = "Péssima"

    if 26 <= produto <= 50:
        qualidade = "Ruim"
    
    if 51 <= produto <= 70:
        qualidade = "Razoável"

    if 71 <= produto <= 90:
        qualidade = "Boa"
    
    if 91 <= produto <= 100:
        qualidade = "Ótima"
    
    return qualidade

#Lista de Teste


sensores = [
    sensoresEstacao(id_estacao="sensor_01", oxigenio_dissolvido=4.2, turbidez=5.2, temperatura=36.0, condutividade=1000.0, amonio=0.6, pH=6.2),
    sensoresEstacao(id_estacao="sensor_02", oxigenio_dissolvido=3.8, turbidez=4.5, temperatura=32.0, condutividade=800.0, amonio=0.45, pH=9.6),
    sensoresEstacao(id_estacao="sensor_03", oxigenio_dissolvido=6.3, turbidez=3.0, temperatura=22.0, condutividade=600.0, amonio=0.3, pH=7.7),
    sensoresEstacao(id_estacao="sensor_04", oxigenio_dissolvido=2.0, turbidez=4.8, temperatura=33.5, condutividade=950.0, amonio=0.55, pH=6.0),
    sensoresEstacao(id_estacao="sensor_05", oxigenio_dissolvido=9.2, turbidez=1.0, temperatura=40.0, condutividade=670.0, amonio=0.2, pH=8.2),
    sensoresEstacao(id_estacao="sensor_06", oxigenio_dissolvido=5.7, turbidez=1.5, temperatura=30.5, condutividade=500.0, amonio=0.4, pH=8.7),
    sensoresEstacao(id_estacao="sensor_07", oxigenio_dissolvido=3.4, turbidez=4.3, temperatura=28.2, condutividade=420.0, amonio=0.48, pH=9.3),
    sensoresEstacao(id_estacao="sensor_08", oxigenio_dissolvido=4.5, turbidez=5.0, temperatura=24.0, condutividade=530.0, amonio=0.3, pH=6.9),
    sensoresEstacao(id_estacao="sensor_09", oxigenio_dissolvido=3.0, turbidez=4.0, temperatura=35.0, condutividade=800.0, amonio=0.35, pH=7.5),
    sensoresEstacao(id_estacao="sensor_10", oxigenio_dissolvido=7.4, turbidez=1.8, temperatura=25.0, condutividade=600.0, amonio=0.45, pH=7.8),
    sensoresEstacao(id_estacao="sensor_11", oxigenio_dissolvido=5.0, turbidez=2.7, temperatura=27.0, condutividade=680.0, amonio=0.42, pH=8.5),
    sensoresEstacao(id_estacao="sensor_12", oxigenio_dissolvido=4.3, turbidez=3.4, temperatura=37.0, condutividade=900.0, amonio=0.5, pH=6.7),
    sensoresEstacao(id_estacao="sensor_13", oxigenio_dissolvido=8.1, turbidez=2.2, temperatura=29.0, condutividade=550.0, amonio=0.3, pH=8.0),
    sensoresEstacao(id_estacao="sensor_14", oxigenio_dissolvido=2.5, turbidez=3.8, temperatura=31.5, condutividade=700.0, amonio=0.38, pH=6.4),
    sensoresEstacao(id_estacao="sensor_15", oxigenio_dissolvido=7.6, turbidez=2.0, temperatura=26.0, condutividade=650.0, amonio=0.4, pH=8.3)
]

for sns in sensores:
    prod_Teste = nota_qualidade_agua(sns, pesos, limites)
    print("Nota:", "{:.3f}".format(round(prod_Teste, 3)), "--- Avaliação:", qualificar_agua(prod_Teste))