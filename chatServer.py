__author__ = 'raul'

import socket,select

def broadcast_msg(sock, msg):
    for socket in connectionList:
        if socket != server and socket != sock:
            try:
                socket.send(msg)
            except:
                socket.close()
                connectionList.remove(socket)



if __name__ == "__main__":

    connectionList = []
    msgBuffer = 4096

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 6969))
    server.listen(10)

    connectionList.append(server)
    print "Servidor iniciado"

    while 1:
        read_sockets,write_sockets,error_sockets = select.select(connectionList,[],[])
        for sock in read_sockets:
            if sock == server:
                client, addr = server.accept()
                connectionList.append(client)
                print "Usuario (%s:%s) conectado" %addr
                broadcast_msg(client,"(%s:%s) entro a la sala \n" %addr)

            else:
                try:
                    data = sock.recv(msgBuffer)
                    if data:
                        broadcast_msg(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)

                except:
                    broadcast_msg(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    connectionList.remove(sock)
                    continue

server.close()