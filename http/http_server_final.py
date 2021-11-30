# Importa módulo socket, que forma base das comunicações em rede em Python
import socket as sk
import sys
import time
import os

responses = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this resource.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }

DEFAULT_ERROR_MESSAGE = """\
<head>
<title>Error response</title>
</head>
<body>
<h1>Error response</h1>
<p>Error code {}.
<p>Message: {}.
</body>
"""

http_head_eg = """
HTTP/1.1 \r\n 
Server: 0.0.0.0:8081 \r\n 
Content-Type: null \r\n 
Date: Hoje \r\n
"""

http_head_format = """
HTTP/%(http_version)s \r\n 
Server: %(server_add)s \r\n 
Content-Type: %(content_type)s \r\n 
Date: Hoje \r\n
"""


# deve-se usar: html.format(TITULO,MENSAGEM)
html = """
<!DOCTYPE html> \r\n 
<html> \r\n 
<head> \r\n 
<title>Page Title</title> \r\n 
</head> \r\n 
<body> \r\n 

<h1>{}</h1> \r\n 
{}

</body> \r\n 
</html> \r\n 
"""
base_link = ''

# Define número de porta do processo servidor
serverPort = 8081

# Cria soquete TCP do servidor
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM) # Define TCP
serverSocket.bind(('', serverPort)) 

# Servidor aguarda requisições de conexão TCP de cliente (parâmetro especifica número máximo de conexões em fila)
serverSocket.listen(10)
print('Servidor pronto para receber!')



def analise_msg(message_in=''):
    if message_in != '':
        msg_split = message_in.split(' ')
        funcao = msg_split[0]
        diretorio = msg_split[1]
        if funcao == 'GET':
            print("Função " + funcao + " no diretório " + diretorio)
            pass
        return funcao, diretorio
        pass
    return '',''
    pass


def search_path(args):
    # global base_link
    titulo = ''
    l = ''
    aux_path = os.getcwd()
    path = aux_path + args[1:]

    if os.path.exists(path) == 0:
        print(path)
        l = 'ERRO!'
        return l
        pass



    # if os.path.isfile(path):
    #     f = open(path,'r')
    #     for line in f:
    #         l = l + line
    #         pass
    #     f.close()
    #     pass
    if os.path.isfile(path):
        nome_do_arquivo = path.split('/')[::-1][0]
        titulo = 'Mostrando Arquivo: <b>' + nome_do_arquivo + '</b>'

        # link = '/home'
        link = args[:-(len(nome_do_arquivo) + 1)]
        nova_linha = '<p><a href="http://127.0.0.1:{}' + link + '">' + '/voltar' + '</a></p>'
        l = l + nova_linha.format(str(serverPort)) + ' \r\n ' + ' \r\n '
        
        f = open(path,'r')
        # <p>{}</p> \r\n 
        for line in f:
            l = l + '<p>' + line + '</p> \r\n \r\n '
            pass
        f.close()
        pass

    elif os.path.isdir(path):
        nome_do_arquivo = path.split('/')[::-1][0]
        titulo = 'Mostrando Diretorio: <b>' + nome_do_arquivo + '</b>'
        link = args[:-(len(nome_do_arquivo) + 1)]
        if link != '':
            nova_linha = '<p><a href="http://127.0.0.1:{}' + link + '">' + '/voltar' + '</a></p>'
            l = l + nova_linha.format(str(serverPort)) + ' \r\n '
            pass
        # nova_linha = '<p><a href="http://127.0.0.1:{}' + link + '">' + '/voltar' + '</a></p>'


        ls = os.listdir(path)
        for x in ls:
            link = x
            nova_linha = '<p><a href="http://127.0.0.1:{}/' + link + '">' + '/' + link + '</a></p>'
            l = l + nova_linha.format(str(serverPort)+args) + ' \r\n '
            pass
        pass
    return html.format(titulo,l)


while 1:

    # accept() aceita conexão com cliente e cria soquete provisório
    connectionSocket, addr = serverSocket.accept()

    # recv() recebe mensagem pelo soquete
    message_in = connectionSocket.recv(4096) 
    
    # Prepara mensagem a ser enviada pelo servidor
    funcao, diretorio = analise_msg(message_in=message_in.decode('utf-8'))
    file = search_path(diretorio)
    if file == 'ERRO!':
        code = 404
        short, message = responses[code]

        msg = http_head_eg + DEFAULT_ERROR_MESSAGE.format(code, message) + '\r\n\r\n'
    else:
        msg = http_head_eg + file + '\r\n\r\n'
        pass

    
    # send() envia mensagem modificada ao cliente pelo soquete
    connectionSocket.send(msg.encode('utf-8'))
    
    # Fecha soquete provisório de conexão com cliente
    connectionSocket.close()
    pass

