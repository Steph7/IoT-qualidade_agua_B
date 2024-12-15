import socket
import threading

# Função que trata a comunicação com cada cliente
def handle_client(conn, addr):
    print(f"Nova conexão de {addr}")
    
    # Recebe dados do cliente
    data = conn.recv(1024)
    if data:
        print(f"Mensagem recebida do cliente {addr}: {data.decode()}")
        
        # Envia uma resposta para o cliente
        conn.sendall(b"Mensagem recebida com sucesso!")
    
    # Fecha a conexão com o cliente
    conn.close()

# Função que cria e gerencia o servidor
def start_server():
    HOST = '127.0.0.1'  # Endereço local
    PORT = 65432        # Porta para o servidor escutar

    # Cria um socket de servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor aguardando conexões em {HOST}:{PORT}...")

        while True:
            # Aguarda uma conexão de um cliente
            conn, addr = server_socket.accept()

            # Cria uma nova thread para cada cliente
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
