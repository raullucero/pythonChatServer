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
                del usersMap[socket]

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

                username = client.recv(1024)
                usersMap[client]= (username, server)
                print "Usuario %s@%s conectado" %(addr, username)
                broadcast_msg(client,"(%s) entro a la sala \n" %username)

            else:
                try:
                    data = sock.recv(msgBuffer)
                    newdata = data[0:len(data)-1];
                    if newdata == "/list":
                        sock.send("Lista de usuarios en linea\n")
                        for seleted_sock, Utuple in usersMap.iteritems():
                            name, SSock = Utuple
                            sock.send(name+'\n')

                    elif newdata == "/off":
                        name, selected_sock = usersMap[sock]
                        if selected_sock != server:
                            tname, ttsock = usersMap[selected_sock]
                            usersMap[selected_sock] = (tname, server)
                            selected_sock.send('Usuario (%s) se ha desconectado\n' %name)
                        sock.send('\rTe desconectaste\n')
                        msg = 'Usuario (%s) se ha desconectado\n' %name
                        print "Usuario %s se desconecto" %name
                        del usersMap[sock]
                        broadcast_msg(sock, msg)
                        sock.close()
                        connectionList.remove(sock)

                    elif newdata[0:1] == "@":
                        sName, TSock = usersMap[sock]
                        for seleted_sock, Utuple in usersMap.iteritems():
                            name, SSock = Utuple
                            if name ==newdata[1:] and SSock == server and seleted_sock != sock:
                                sock.send('\rEstas chateando con %s\n' % name)
                                usersMap[sock] = (sName, seleted_sock)
                                seleted_sock.send('\rEstas chateando con %s\n' % sName)
                                usersMap[seleted_sock] = (name, sock)

                    elif newdata[0:5] == "/exit":
                        name, selected_sock = usersMap[sock]
                        if selected_sock != usersMap[sock]:
                            selected_name, select_sock_selected = usersMap[selected_sock]
                            usersMap[selected_sock] = (selected_name, server)
                            usersMap[sock] = (name, server)
                            sock.send('\rTe desconectaste del chat privado\n')
                            selected_sock.send('\r%s dejo el chat privado\n' % name)

                    elif newdata == "/help":
                        sock.send("Usa los distinos comandos\n")
                        sock.send("El comando /list te ayudara a ver quien esta conectado \n")
                        sock.send("El comando @Usuario te ayudara a tener un chat privado con el usuario que elijas\n")
                        sock.send("El comando /exit si ya estas en un chat privado este comando te ayudara a salir del chat y volver a la sala\n")
                        sock.send("El comando /off te ayudara a salir del servidor \n")

                    else:
                        #Send a msn
                        uName, tSock = usersMap[sock]
                        newmessage = '%s: %s' % (uName, data)
                        if tSock != server:
                            tSock.send(newmessage)

                except:
                    uName, tSock = usersMap[sock]
                    broadcast_msg(sock, "Usuario (%s) se ha desconectado\n" %uName)
                    print "Usuario @%s se desconecto" %uName
                    del usersMap[sock]
                    sock.close()
                    connectionList.remove(sock)
                    continue

server.close()