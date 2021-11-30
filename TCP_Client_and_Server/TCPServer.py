# -*- coding: utf-8 -*-

# Importa módulo socket, que forma base das comunicações em rede em Python
import socket as sk

# Define número de porta do processo servidor
serverPort = 8081#12000

# Cria soquete TCP do servidor
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM) 
serverSocket.bind(('', serverPort)) 

# Servidor aguarda requisições de conexão TCP de cliente (parâmetro especifica número máximo de conexões em fila)
serverSocket.listen(10)

print('Servidor pronto para receber!')

x = 0
#for x in range(1,10):
while x != 'break':
	x = x + 1
	print ("Esta é a vez número ", str(x)," Por vavor aproveite nosso serviço!")

    # accept() aceita conexão com cliente e cria soquete provisório
	
	connectionSocket, addr = serverSocket.accept()
	# recv() recebe mensagem pelo soquete
	message = connectionSocket.recv(4096) 
	
	# Coloca string em maiúsculas
	modifiedMessage = message.decode(format(message)).upper()
	
	# send() envia mensagem modificada ao cliente pelo soquete
	connectionSocket.send(modifiedMessage.encode(format(message)))
	
	# Fecha soquete provisório de conexão com cliente
	connectionSocket.close()
	x = 'break'
	if modifiedMessage == 'EXIT':
		print('Servidor encerrado...')
		pass
	pass
print('Servidor encerrando...')
serverSocket.close()