__author__ = 'raul lucero'
import socket,select

def broadcast_msg(sock, msg, chat):
    for socket in connectionList:
        if socket != server and socket != sock and chat == "publico":
            try:
                socket.send(msg)
            except:
                socket.close()
                connectionList.remove(socket)
    for socket in connectionList:
        if socket == sock and chat == "privado":
            socket.send(msg)       
                

def get_user(client):
    info = usersMap[client]
    name = info[1]
    return name

if __name__ == "__main__":

    connectionList = []
    privadeList = []
    msgBuffer = 4096
    usersMap = {}
    chat = "publico"
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
                chat = "publico"
                broadcast_msg(client,"(%s) entro a la sala \n" %get_user(client),chat)

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
                                chat = "privado"
                                privadeList.append(source)
                                privadeList.append(end)
                                source.send("Chat privado con %s\n" %us_end)
                                end.send("Chat privado con %s\n" %us_source)
                                while 1:
                                    for s in privadeList:
                                        msg = s.recv(2046)
                                        if s != source:
                                            if s == end:
                                                tempo = source
                                                source = s
                                                end = tempo
                                            else:
                                                print "Error"
                                        if msg:
                                            broadcast_msg(end,"\r"  + get_user(s)+ ' : '+ msg,chat)
                                
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