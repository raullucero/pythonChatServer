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

def get_user(client):
    info = usersMap[client]
    name = info[1]
    return name



if __name__ == "__main__":

    connectionList = []
    msgBuffer = 4096

    usersMap = {}


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
                usersMap[client]= addr,client.recv(1024)
                print "Usuario %s@%s conectado" %(addr, get_user(client))

                broadcast_msg(client,"(%s) entro a la sala \n" %get_user(client))

            else:
                try:
                    data = sock.recv(msgBuffer)
                    newdata = data[0:len(data)-1];
                    if newdata == "/list":
                        client.send("Lista de usuarios en linea\n")
                        for us in usersMap.items():
                             client.send(str(us[1][1])+"\n")





                except:
                    broadcast_msg(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    connectionList.remove(sock)
                    continue

server.close()