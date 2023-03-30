import socket
from threading import Thread


class PortDescriptor:
    def __init__(self, default_port=7777):
        self._port = default_port

    def __get__(self, instance, owner):
        return self._port

    def __set__(self, instance, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Port number must be a non-negative integer")
        self._port = value


class ClientVerifier(type):
    def __init__(cls, name, bases, attrs):
        for name, attr in attrs.items():
            if name == "accept" or name == "listen":
                if callable(attr):
                    raise TypeError(f"Method {name} of socket cannot be used in class {cls.__name__}")
            elif name == "socket":
                if not isinstance(attr, socket.socket):
                    raise TypeError(f"socket attribute of class {cls.__name__} must be a socket object")
                if attr.family != socket.AF_INET or attr.type != socket.SOCK_STREAM:
                    raise TypeError(f"socket attribute of class {cls.__name__} must be a TCP socket")


class ServerVerifier(type):
    def __init__(cls, name, bases, attrs):
        for name, attr in attrs.items():
            if name == "connect":
                if callable(attr):
                    raise TypeError(f"Method {name} of socket cannot be used in class {cls.__name__}")
            elif name == "socket":
                if not isinstance(attr, socket.socket):
                    raise TypeError(f"socket attribute of class {cls.__name__} must be a socket object")
                if attr.family != socket.AF_INET or attr.type != socket.SOCK_STREAM:
                    raise TypeError(f"socket attribute of class {cls.__name__} must be a TCP socket")


class Client(metaclass=ClientVerifier):
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send(self, message):
        self.socket.sendall(message.encode())

    def receive(self):
        return self.socket.recv(1024).decode()

    def close(self):
        self.socket.close()


class Server(metaclass=ServerVerifier):
    class Port(PortDescriptor):
        pass

    def __init__(self, port=7777):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", port))
        self.socket.listen(1)
        self.clients = []
        self.running = True

    def start(self):
        while self.running:
            conn, addr = self.socket.accept()
            client = ClientHandler(conn, addr)
            client.start()
            self.clients.append(client)

    def stop(self):
        self.running = False
        self.socket.close()
        for client in self.clients:
            client.close()


class ClientHandler(Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self):
        while True:
            message = self.conn.recv(1024)
            if not message:
                break
            for client in Server.clients:
                client.conn.sendall(message)
        self.conn.close()