import socket

from gui import ChatWindow, AdminWindow
from PyQt5.QtWidgets import QApplication


class Client:
    """Represents a client that connects to a server and sends/receives messages.

    Attributes:
        host (str): The server hostname.
        port (int): The server port.
        sock (:obj:`socket.socket`): The client socket.

    """

    def __init__(self, host, port):
        """Initializes a new instance of the Client class.

        Args:
            host (str): The server hostname.
            port (int): The server port.

        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connects to the server."""
        self.sock.connect((self.host, self.port))

    def send(self, message):
        """Sends a message to the server and receives the response.

        Args:
            message (str): The message to send.

        Returns:
            str: The server response.

        """
        self.sock.sendall(message.encode())
        data = self.sock.recv(1024)
        return data.decode()

    def close(self):
        """Closes the client socket."""
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
