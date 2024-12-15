import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço local (mesmo que o servidor)
PORT = 65432        # A mesma porta do servidor

# Cria um socket de cliente
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Conecta ao servidor
    s.connect((HOST, PORT))
    
    # Envia uma mensagem para o servidor
    message = "Olá, servidor!"
    s.sendall(message.encode())
    
    # Recebe a resposta do servidor
    data = s.recv(1024)
    
    print(f"Resposta do servidor: {data.decode()}")
