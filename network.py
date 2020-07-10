import socket
from _thread import *

class Network:

    HEADER = 10
    IP = '192.168.56.1'
    PORT = 5575
    ADDR = (IP, PORT)
    BUFFER = 512

    def __init__(self, id):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.en_id = str(id).encode('utf-8')
        self.client_socket.send(self.en_id)
        self.lock = allocate_lock()
        self.msgs = []
        self.backup = []
        start_new_thread(self.receive_msg, ())

    def send_msg(self, msg):
        self.message = msg.encode('utf-8')
        self.msg_length  = len(self.message)
        self.send_length = str(self.msg_length).encode('utf-8')
        self.send_length += b' ' * (self.HEADER - len(self.send_length))
        self.client_socket.send(self.send_length)
        self.client_socket.send(self.message)


    def receive_msg(self):
        while True:
            try:
                msg_length = self.client_socket.recv(self.BUFFER).decode('utf-8')
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.client_socket.recv(msg_length).decode('utf-8')
                    self.lock.acquire()
                    self.msgs.append(msg)
                    self.backup.append(msg)
                    self.lock.release()

            except Exception as e:
                break

    def disconnect(self):
        msg = "DISCONNECT"
        self.send_msg(msg)