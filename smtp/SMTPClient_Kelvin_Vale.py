# O e-mail usado nesta atividade foi criado único e exclusivamente para 
#  a execução da mesma.

# Importa módulo socket, que forma base das comunicações em rede em Python
import socket as sk
# Importa módulo base64, que forma codifica mensagem texto em binário de 64 bits
import base64 as b64
# Importa módulo sst, que implementa camada de soquete de segurança (criptografia)
import ssl

import os


# Define nome (ou IP) e número de porta do servidor SMTP
serverName = 'smtp.gmail.com'
serverPort = 587

# Cria soquete TCP do cliente
clientSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

# Solicita estabelecimento de conexão com servidor
clientSocket.connect((serverName, serverPort))
recv = clientSocket.recv(1024) # Aguarda confirmação 220 do servidor
print(recv.decode('utf-8'))

# Envia mensagem HELO para servidor
clientSocket.send('HELO gmail.com\r\n'.encode('utf-8'))
recv = clientSocket.recv(1024) # Aguarda confirmação 250 do servidor
print(recv.decode('utf-8'))

# Inicia sessão TLS com servidor
clientSocket.send('STARTTLS\r\n'.encode('utf-8'))
recv = clientSocket.recv(1024) # Aguarda confirmação 220 do servidor
print(recv.decode('utf-8'))

# Cria soquete seguro e solicita login com servidor via sessão TLS
secureclientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
secureclientSocket.send('AUTH LOGIN\r\n'.encode('utf-8'))
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
msg_in = recv.decode('utf-8')
print(msg_in)

# Envia nome de usuário ao servidor via sessão TLS
secureclientSocket.send(b64.b64encode('computadoresredede88@gmail.com'.encode('utf-8')) + '\r\n'.encode('utf-8'))
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
print(recv.decode('utf-8'))

# Envia senha ao servidor via sessão TLS
SENHA = 'SenhaPAraTestE_5863'
SENHA = b64.b64encode(SENHA.encode('utf-8'))
secureclientSocket.send(SENHA + '\r\n'.encode('utf-8'))
recv = secureclientSocket.recv(1024) # Aguarda confirmação 235 do servidor
print(recv.decode('utf-8'))

# Define o remetente
msg = 'MAIL FROM: <computadoresredede88@gmail.com>\r\n'.encode('utf-8')
secureclientSocket.send(msg)
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
msg_in = recv.decode('utf-8')
print(msg_in)

# Define o destinatário
msg = 'RCPT TO: <kelvindv3@gmail.com>\r\n'.encode('utf-8')
secureclientSocket.send(msg)
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
msg_in = recv.decode('utf-8')
print(msg_in)

# Define o destinatário
msg = 'RCPT TO: <kelvin.vale@ee.ufcg.edu.br>\r\n'.encode('utf-8')
secureclientSocket.send(msg)
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
msg_in = recv.decode('utf-8')
print(msg_in)

# Define o destinatário
msg = 'RCPT TO: <leocarlos@dee.ufcg.edu.br>\r\n'.encode('utf-8')
secureclientSocket.send(msg)
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
msg_in = recv.decode('utf-8')
print(msg_in)

# Define o início da transmissão da menssagem
msg = 'DATA\r\n'.encode('utf-8')
secureclientSocket.send(msg)
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
msg_in = recv.decode('utf-8')
print(msg_in)

# Começo do texto da menssagem
message_o = ('Boa noite professor, este é o código da minha atividade SMTP em execução\n\r\n').encode('utf-8')
secureclientSocket.send(message_o)

message_o = ('Aluno - Kelvin Dantas Vale\r\n').encode('utf-8')
secureclientSocket.send(message_o)

message_o = ('Matrícula - 115111757\n\r\n').encode('utf-8')
secureclientSocket.send(message_o)

message_o = ('OBS - Os e-mails listados são os meus e o do senhor\n\n\r\n').encode('utf-8')
secureclientSocket.send(message_o)

# Abrindo o arquivo para enviar este documento
path = os.getcwd()
arq_name = 'SMTPClient_Kelvin_Vale.py'
arq = open(path + '/' + arq_name, 'r')
for i in arq.readlines():
	msg = (i).encode('utf-8')
	secureclientSocket.send(msg)
	pass
arq.close()

# Fim do texto da menssagem ! Pelo protocolo, a menssagem se encerra com o ponto!
message_o = ('\r\n.\r\n').encode('utf-8')
secureclientSocket.send(message_o)
recv = secureclientSocket.recv(1024)
print(recv.decode('utf-8'))

# Determina o fim da comunicação
msg = 'QUIT\r\n'.encode('utf-8')
secureclientSocket.send(msg)
recv = secureclientSocket.recv(1024)
msg_in = recv.decode('utf-8')
print(msg_in)

# Fecha soquete SSL do cliente
secureclientSocket.close()

# Fecha soquete do cliente
clientSocket.close()