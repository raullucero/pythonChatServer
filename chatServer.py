from dummy_thread import start_new_thread

__author__ = 'raul lucero'

import socket,select

def broadcast_msg(sock, msg):
    for socket in connectionList:
        if socket != server and socket != sock:
            try:
                socket.send(msg)
            except:
                socket.close()
                connectionList.remove(socket)
                prueba.remove(socket)

def broadcast_PrivateChat(sock2 , msg):
    for socket in prueba:
        if socket == sock2:
            sock2.send(msg)


def get_user(client):
    info = usersMap[client]
    name = info[1]
    return name

def clientthread(source, end, us_source, us_end):

    source.send("Chat privado con %s\n" %us_end)
    end.send("Chat privado con %s\n" %us_source)
    ex = 1

    while ex:
        read_sockets,write_sockets,error_sockets = select.select(prueba,[],[])
        for SOCKET in read_sockets:
            msg = SOCKET.recv(2048)
            if SOCKET != source:
                if SOCKET == end:
                    user_func = str(us_end)
                    tempo = source
                    source = SOCKET
                    end = tempo
                else:
                    print "Error"
            if msg:

                if msg[0:5] == "/exit":
                    source.send("\rEl chat con "  + get_user(end)+ ' termino \n')
                    connectionList.append(source)
                    connectionList.append(end)
                    end.send("\rEl chat con "  + get_user(SOCKET)+ ' termino \n')
                    ex = 0
                    break



                else:
                    broadcast_PrivateChat(end,"\r"  + get_user(SOCKET)+ ' : '+ msg)


if __name__ == "__main__":

    connectionList = []
    msgBuffer = 4096
    prueba = []
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
                prueba = connectionList
                usersMap[client]= addr,client.recv(1024)
                print "Usuario %s@%s conectado" %(addr, get_user(client))

                broadcast_msg(client,"(%s) entro a la sala \n" %get_user(client))

            else:
                try:
                    data = sock.recv(msgBuffer)
                    newdata = data[0:len(data)-1];
                    if newdata == "/list":
                        sock.send("Lista de usuarios en linea\n")
                        for us in usersMap.items():
                             sock.send(str(us[1][1])+"\n")
                    if newdata[0:1] == "@":
                        for us in usersMap.items():
                            if(us[1][1]==newdata[1:]):
                                source = sock
                                end = us[0]
                                us_source = usersMap[sock][1]
                                us_end = us[1][1]
                                #private_chat(source,end,us_source,us_end)
                                start_new_thread(clientthread(source,end,us_source,us_end))
                            else:
                                finded = 1
                        if finded == 1:
                            sock.send("\nNo se encontro el usuario ")

                except:
                    broadcast_msg(sock, "Usuario (%s) se ha desconectado\n" %get_user(sock))
                    print "Usuario %s@%s se desconecto" %(addr, get_user(sock))
                    del usersMap[sock]
                    sock.close()
                    connectionList.remove(sock)
                    continue

server.close()