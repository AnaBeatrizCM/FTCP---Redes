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
        print(resposta.decode('utf-8'))
    except socket.timeout as e:
        print("Timed out")


if __name__ == '__main__':
    udp()
