import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))

    def send(self, message):
        self.sock.sendall(message.encode())
        data = self.sock.recv(1024)
        return data.decode()

    def close(self):
        self.sock.close()


client = Client("localhost", 8888)
client.connect()
client.send("test message")
client.close()
