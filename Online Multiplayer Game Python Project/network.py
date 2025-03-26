import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return int(self.client.recv(2048).decode())
        except:
            print("Connection Failed!")
            return None

    def send(self, data):
        self.client.send(str.encode(data))
        return self.client.recv(2048).decode()
