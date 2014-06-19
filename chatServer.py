__author__ = 'raul'

import socket,select

if __name__ == "__main__":
#Declaramos la lista de conexiones que se conecten al servidor y el buffer de mensajes
    connectionList = []
    msgBuffer = 4096

    server = socket.socket((socket.AF_INET, socket.SOCK_STREAM))#Se crea el socket del servidor
    server.sockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)#ReaseADDR dice que reuse el socket
    server.bind(("", 6969)) # se conecta al localhost y al puerto 6969

    connectionList.append(server)
    print "Servidor iniciado"

    while 1:
        read_sockets,write_sockets,error_sockets = select.select(connectionList,[],[])
        for sock in read_sockets:
            if sock == server:
                client, addr = server.accept()
                connectionList.append(client)

server.close()