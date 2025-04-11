import threading
import socket


PORT = 3000
SERVER_PORT = 5002


def udp():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('127.0.0.1', PORT))
    udp_sock.settimeout(5)
    print(f"UDP server listening on port {PORT}")

    arquive = input("Arquivo: ")
    data = "REQUEST,TCP," + arquive
    udp_sock.sendto(data.encode('utf-8'), ('127.0.0.1', SERVER_PORT))

    try:
        resposta, addr = udp_sock.recvfrom(1024)
        resposta = resposta.decode('utf-8')
        print(resposta)

        parte = resposta.split(',')

        if parte[0] == "RESPONSE" and parte[1] == "TCP":
            tcp_port = int(parte[2])
            filename = parte[3].strip()
            tcp(tcp_port, filename)
        else:
            print("Resposta inesperada:", resposta)

    except socket.timeout as e:
        print("Timed out")

def tcp(tcp_port, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        tcp_sock.connect(('127.0.0.1', tcp_port))
        print(f"Conectado ao servidor TCP na porta {tcp_port}")

        get_cmd = f"GET {filename}"
        tcp_sock.sendall(get_cmd.encode('utf-8'))
        data = tcp_sock.recv(4096).decode('utf-8')
        print(f"Conteúdo recebido:\n{data}")

        tcp_sock.sendall("ACK".encode('utf-8'))
        print("ACK enviado. Conexão encerrada.")

if __name__ == '__main__':
    udp()
