import json
import select
import socket
import sys
from server_log_config import logger
from log_decorator import log


class Server:
    def __init__(self, address='', port=7777):
        self.address = address
        self.port = port
        self.connections = []
        self.sock = None

    def send_all(self, message):
        for conn in self.connections:
            self.send_response(conn, message)

    def handle_message(self, message, conn):
        if message['action'] == 'presence':
            response = self.handle_presence_message(message)
            self.send_response(conn, response)
        elif message['action'] == 'msg':
            self.send_all(message)

    @log
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            self.sock.bind((self.address, self.port))
            self.sock.listen(10)
            self.connections.append(self.sock)

            logger.info(f'Server started on {self.address}:{self.port}')

            while True:
                read_sockets, _, _ = select.select(self.connections, [], [])

                for sock in read_sockets:
                    if sock == self.sock:
                        conn, addr = self.sock.accept()
                        self.connections.append(conn)
                        logger.info(f'Client connected: {addr}')

                    else:
                        try:
                            message = self.receive_message(sock)
                            self.handle_message(message, sock)
                        except Exception as e:
                            logger.exception(f'Error handling message from {sock.getpeername()}: {e}')
                            self.connections.remove(sock)
                            sock.close()

    def send_response(self, sock, response):
        encoded_response = json.dumps(response).encode('utf-8')
        sock.send(encoded_response)
        logger.info(f'Sent response: {response}')

    def receive_message(self, sock):
        encoded_message = sock.recv(4096)
        message = json.loads(encoded_message.decode('utf-8'))
        logger.info(f'Received message: {message}')
        return message

    def handle_presence_message(self, message):
        response = {
            'response': 200,
            'time': message['time'],
            'alert': 'OK'
        }
        logger.info(f'Handled presence message: {message}')
        return response
