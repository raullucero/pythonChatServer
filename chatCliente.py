__author__ = 'raul'

def cursor():
    sys.stdout.write(">: ")
    sys.stdout.flush()


import socket, select, sys

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.settimeout(2)
try:
    cliente.connect(("localhost",6969))
except:
    print "No se pudo establecer la conexion"
    sys.exit()

print "Bienvenido a la sala de chat "
cursor()

while 1:
    socketList = [sys.stdin, cliente]
    read_sockets, write_sockets, error_sockets = select.select(socketList , [], [])

    for sock in read_sockets:
        if sock == cliente:
            data = sock.recv(4096)
            if not data:
                print "\nDesconectado del servidor"
                sys.exit()
            else:
                sys.stdout.write(data)
                cursor()
        else:
                msg = sys.stdin.readline()
                cliente.send(msg)
                cursor()