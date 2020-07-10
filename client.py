import random
import string

class Client:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.id = None

    def getConn(self):
        return self.conn

    def getAddr(self):
        return self.addr

    def setConn(self, conn):
        self.conn = conn

    def setAddr(self, addr):
        self.addr = addr

    def setId(self, id):
        self.id = id

    def __str__(self):
       return f"{self.id} : {self.addr}"