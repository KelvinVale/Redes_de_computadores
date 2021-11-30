#client_sock.py
import socket

HOST = 'localhost' #coloca o host do servidor
PORT = 57000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((HOST,PORT))
arq = open('/home/kelvin/Área de Trabalho/redes_de_computadores/k.py', 'r')

for i in arq.readlines():
	msg = i.encode('utf-8')
	s.send(msg)

arq.close()
s.close()