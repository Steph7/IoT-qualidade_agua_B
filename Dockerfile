# Use a imagem base Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o requirements.txt para o container
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do projeto para o container
COPY . .

# Dê permissão para o script run_both.sh ser executado
RUN chmod +x /venv/src/run_both.sh

# Comando para rodar o script que executa ambos os programas
CMD ["/bin/bash", "/venv/src/run_both.sh"]