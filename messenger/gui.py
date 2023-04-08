import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from client import Client


class ChatWindow(QtWidgets.QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setWindowTitle("Chat")
        self.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.chat_history = QtWidgets.QTextEdit(self.centralwidget)
        self.chat_history.setReadOnly(True)
        self.verticalLayout.addWidget(self.chat_history)
        self.message_input = QtWidgets.QLineEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.message_input)
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setText("Send")
        self.verticalLayout.addWidget(self.send_button)
        self.setCentralWidget(self.centralwidget)

        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_button.click)

        self.show()

    def send_message(self):
        message = self.message_input.text()
        if message:
            response = self.client.send(message)
            self.chat_history.append(response)
            self.message_input.clear()


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setWindowTitle("Admin Panel")
        self.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.clients_list = QtWidgets.QListWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.clients_list)
        self.statistics_label = QtWidgets.QLabel(self.centralwidget)
        self.verticalLayout.addWidget(self.statistics_label)
        self.setCentralWidget(self.centralwidget)

        self.update_clients_list()
        self.update_statistics()

        self.show()

    def update_clients_list(self):
        response = self.client.send("get_clients")
        if response:
            clients = response.split(",")
            self.clients_list.clear()
            self.clients_list.addItems(clients)

    def update_statistics(self):
        response = self.client.send("get_statistics")
        if response:
            self.statistics_label.setText(response)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    client = Client("localhost", 8888)
    client.connect()

    chat_window = ChatWindow(client)
    admin_window = AdminWindow(client)

    sys.exit(app.exec_())
