import json

# Função para salvar dados em um arquivo JSON
def salvar_dados(dados, arquivo='dados.json'):
    with open(arquivo, 'w') as f:
        json.dump(dados, f)

# Função para carregar dados de um arquivo JSON
def carregar_dados(arquivo='dados.json'):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Exemplo de uso
dados = {"nome": "Maria", "idade": 30}
salvar_dados(dados)

# Carregar e mostrar dados
dados_carregados = carregar_dados()
print(dados_carregados)
