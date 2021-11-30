# -*- coding: utf-8 -*-

# Importa módulo socket, que forma base das comunicações em rede em Python
import socket as sk

# Define número de porta do processo servidor
serverPort = 12000

# Cria soquete UDP do servidor
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM) 
serverSocket.bind(('', serverPort)) 

print('Servidor pronto para receber!')

while 1:
    
    # recvfrom() recebe mensagem pelo soquete
    message, clientAddress = serverSocket.recvfrom(2048) 
    message = 'Resposta: ' + message.decode('utf-8')

    # Coloca string em maiúsculas
    modifiedMessage = message.upper()
    
    # sendto() envia mensagem modificada ao cliente pelo soquete
    serverSocket.sendto(modifiedMessage.encode('utf-8'), clientAddress)
    
