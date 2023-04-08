import socket

from gui import ChatWindow, AdminWindow
from PyQt5.QtWidgets import QApplication


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


if __name__ == '__main__':
    app = QApplication([])

    client = Client("localhost", 8888)
    client.connect()

    chat_window = ChatWindow(client)
    admin_window = AdminWindow(client)

    chat_window.show()
    admin_window.show()

    app.exec_()
