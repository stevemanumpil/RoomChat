
class Client:

    def __init__(self, conn, path):
        self.conn = conn
        self.id = None
        self.username = None
        self.path = path

    def getUsername(self):
        return self.username

    def getConn(self):
        return self.conn

    def getId(self):
        return self.id

    def getPath(self):
        return self.path

    def setUsername(self, username):
        self.username = username

    def setConn(self, conn):
        self.conn = conn

    def setId(self, id):
        self.id = id

    def setPath(self, path):
        self.path = path

    def __str__(self):
       return f"{self.id}"