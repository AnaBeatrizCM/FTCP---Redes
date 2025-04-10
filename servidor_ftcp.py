import os
import socket
import threading as t
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

FILE_A = config['SERVER_CONFIG']['FILE_A']
FILE_B = config['SERVER_CONFIG']['FILE_B']
TCP_PORT = config['SERVER_CONFIG']['TCP_PORT']
UDP_PORT = config['SERVER_CONFIG']['UDP_PORT']

files = {
		'a.txt': os.path.join(FILE_A),
		'b.txt': os.path.join(FILE_B)
	} 


def udp():
	udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_sock.bind(('0.0.0.0', int(UDP_PORT)))
	print(f"UDP server listening on port {UDP_PORT}")

	while True:
		data, addr = udp_sock.recvfrom(1024)
		
		if not data:
			continue
		print(f"UDP Received from {addr}: {data.decode('utf-8')}")

		data_decoded = data.decode('utf-8')

		try:
			archive = verify(data_decoded)
	
			response = f"RESPONSE,TCP,{TCP_PORT},{archive}"

			udp_sock.sendto(response.encode('utf-8'), addr)

		except Exception as e:
			error_msg = str(e)
			udp_sock.sendto(error_msg.encode('utf-8'), addr)


def verify(data: str):
	
	lista = data.split(',')

	if len(lista) != 3:
		raise Exception("ERROR,INVALID_FORMAT - Use: REQUEST,TCP,filename.txt")

	if lista[0] != "REQUEST":
		raise Exception("ERROR,INVALID_REQUEST_TYPE - First field must be 'REQUEST'")

	if lista[1] != "TCP":
		raise Exception("ERROR,INVALID_PROTOCOL - Only TCP protocol is supported")

	filename = lista[2].strip()
	if filename not in ['a.txt','b.txt']:
		raise Exception("ERROR,FILE_NOT_AVAILABLE - Available files: a.txt, b.txt")

	return filename


if __name__ == '__main__':
	udp_thread = t.Thread(target=udp)
	udp_thread.daemon = True
	udp_thread.start()

	try:
		while True:
			pass
	except KeyboardInterrupt:
		print("cabou")


