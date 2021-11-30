# -*- coding: utf-8 -*-

# Importa módulo socket, que forma base das comunicações em rede em Python
import socket as sk
import os

# Define número de porta do processo servidor
serverPort = 8080

# Cria soquete TCP do servidor
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM) 
serverSocket.bind(('127.0.0.1', serverPort)) 


serverSocket.listen(10)


	
def estabelecer_coneccao_controle(serverSocket=serverSocket):
	connectionSocket_control, addr = serverSocket.accept()

	msg = '220 (kelvin server 0.1)\n'
	connectionSocket_control.send(msg.encode('utf-8'))

	#
	msg_in = connectionSocket_control.recv(4096)
	msg_in = msg_in.decode('utf-8')
	msg_in = msg_in.split(' ')
	command = msg_in[0]
	name = msg_in[1][:-2]

	#
	msg = '331 Please specify the password.\n'
	connectionSocket_control.send(msg.encode('utf-8'))

	#
	msg_in = connectionSocket_control.recv(4096)
	msg_in = msg_in.decode('utf-8')
	msg_in = msg_in.split(' ')
	command = msg_in[0]
	password = msg_in[1][:-2]

	if name == 'user' and password == 'senha':

		msg = '230 Login successful.\n'
		connectionSocket_control.send(msg.encode('utf-8'))
		
		pass
	else:
		#
		msg = '530 Login incorrect.\n'
		connectionSocket_control.send(msg.encode('utf-8'))

		return 0, connectionSocket_control
		pass

	message = connectionSocket_control.recv(4096) 
	msg_in = message.decode('utf-8')

	print(msg_in)

	msg = '200 UNIX\n'
	connectionSocket_control.send(msg.encode('utf-8'))
	return 1, connectionSocket_control

	# connectionSocket_control.close()
	pass

def exec_PORT(msg_in, connectionSocket_control):
	arg = msg_in[1].split(',')

	serverName = arg[0] + '.' + arg[1] + '.' + arg[2] + '.' + arg[3]
	serverPort = 256*int(arg[4]) + int(arg[5])

	clientSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

	clientSocket.connect((serverName, serverPort))

	msg = '200 conectado \n'
	connectionSocket_control.send(msg.encode('utf-8'))
	return clientSocket
	pass

def exec_STOR(clientSocket, file_name, connectionSocket_control):
	path = os.getcwd()
	arq_name = file_name
	arq = open(path + '/' + arq_name, 'w')
	msg = '125 Data connection already open; transfer starting.\n'
	connectionSocket_control.send(msg.encode('utf-8'))
	while 1:
	    dados = clientSocket.recv(4096)
	    if not dados:
	        break
	    msg = dados.decode('utf-8')
	    arq.write(msg)
	    pass

	arq.close()
	clientSocket.close()

	msg = '226 Closing data connection. Requested file action successful \n'
	connectionSocket_control.send(msg.encode('utf-8'))
	pass

def exec_RETR(clientSocket, file_name, connectionSocket_control):
	path = os.getcwd()
	arq_name = file_name
	arq = open(path + '/' + arq_name, 'r')
	msg = '125 Data connection already open; transfer starting.\n'
	connectionSocket_control.send(msg.encode('utf-8'))

	for i in arq.readlines():
		msg = (i).encode('utf-8')
		clientSocket.send(msg)
		pass

	arq.close()
	
	msg = '226 Closing data connection. Requested file action successful \n'
	connectionSocket_control.send(msg.encode('utf-8'))
	
	clientSocket.close()

	pass



file_name = ''
clientSocket = ''
logged = 0
while 1:
	if not logged:
		logged, connectionSocket_control = estabelecer_coneccao_controle(serverSocket=serverSocket)
		pass
	if not logged:
		connectionSocket_control.close()
		continue
		pass

	msg_in = connectionSocket_control.recv(4096) 
	msg_in = msg_in.decode('utf-8')

	print(msg_in)

	msg_in = msg_in.split(' ')
	command = msg_in[0][0:4]


	if command == 'QUIT':
		msg = '200 Bye bye \n'
		connectionSocket_control.send(msg.encode('utf-8'))
		logged = 0
	elif command == 'PORT':
		clientSocket = exec_PORT(msg_in=msg_in, connectionSocket_control=connectionSocket_control)
	elif command == 'STOR':
		exec_STOR(clientSocket=clientSocket, file_name=msg_in[1][:-2], connectionSocket_control=connectionSocket_control)
	elif command == 'RETR':
		exec_RETR(clientSocket=clientSocket, file_name=msg_in[1][:-2], connectionSocket_control=connectionSocket_control)
		pass

	pass
print('Servidor encerrando...')
serverSocket.close()