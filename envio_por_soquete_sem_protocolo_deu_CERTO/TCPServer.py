#serv_sock.py

import socket
import os

HOST = ''
PORT = 57000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()
path = os.getcwd()
arq_name = 'teste_escrita_1.py'
arq = open(path + '/' + arq_name, 'w')

while 1:
    dados = conn.recv(1024)
    if not dados:
        break
    msg = dados.decode('utf-8')
    arq.write(msg)

arq.close()
conn.close()