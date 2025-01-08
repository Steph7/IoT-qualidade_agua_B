# Usar uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos locais para o diretório de trabalho no contêiner
# Isso copiará o script Python e o arquivo requirements.txt
COPY . /app

# Instalar as dependências do arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão para rodar o script data_collector_agua_v2.py
CMD ["python", "/venv/src/data_collector_agua_v2.py"]
