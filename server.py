import socket
from _thread import *
from client import Client

HEADER = 10
IP = ''
PORT = 5575
ADDR = (IP, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind(ADDR)
except socket.error as e:
    print(e)

server_socket.listen()

clients = []

def disconnect(c, addr, id):
    print(f"Connection from {addr} close")
    for cl in clients:
        if cl.id == id:
            clients.remove(cl)

    c.close()


def client_thread(c, addr):
    person = Client(c, addr)
    id = c.recv(HEADER).decode('utf-8')
    person.setId(id)
    clients.append(person)
    for x in clients:
        print(x)
    while True:
        try:
            msg_length = c.recv(HEADER).decode('utf-8')
            if msg_length:
                msg_length = int(msg_length)
                msg = c.recv(msg_length).decode('utf-8')
                if msg == 'DISCONNECT':
                    return disconnect(c, addr, id)

                print(f"message : {msg} from {person.getAddr()}")

                send_msg = msg.encode('utf-8')
                send_msg_length = len(send_msg)
                send_length = str(send_msg_length).encode('utf-8')
                send_length += b' ' * (HEADER - len(send_length))
                c.sendall(send_length)
                c.sendall(send_msg)

        except Exception as e:
            disconnect(c, addr, id)
            print(e)


while True:
    print("Waiting for connection...")
    c, addr = server_socket.accept()
    start_new_thread(client_thread, (c,addr))
    print("Connected with",addr[0],":", addr[1])

c.close()
server_socket.close()