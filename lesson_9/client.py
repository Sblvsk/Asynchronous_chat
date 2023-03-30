import sys
import socket
import json
from send_message import send_message
from receive_message import receive_message
from log_decorator import log
from client_log_config import logger


class Client:
    def __init__(self, server_address, server_port=7777, account_name='Guest'):
        self.server_address = server_address
        self.server_port = server_port
        self.account_name = account_name

    @log
    def send_chat_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_address, self.server_port))
            encoded_message = json.dumps(message).encode('utf-8')
            sock.send(encoded_message)

    @log
    def receive_chat_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_address, self.server_port))
            encoded_message = sock.recv(4096)
            message = json.loads(encoded_message.decode('utf-8'))
        return message

    def create_presence_message(self):
        message = {
            'action': 'presence',
            'time': 123456.789,
            'user': {
                'account_name': self.account_name,
                'status': 'Online'
            }
        }
        return message

    def create_p2p_message(self, to, message_text, from_user):
        message = {
            'action': 'msg',
            'time': 123456.789,
            'to': to,
            'from': from_user,
            'message': message_text
        }
        return message

    @log
    def run(self):
        presence_message = self.create_presence_message()
        self.send_chat_message(presence_message)

        try:
            response = self.receive_chat_message()
        except Exception as e:
            logger.exception('Error receiving message: %s', e)
        logger.info(f'Response: {self.parse_response(response)}')

        while True:
            chat_message = input('Enter your message: ')
            to_user = input('Enter recipient name: ')
            message = self.create_p2p_message(to_user, chat_message, presence_message['user']['account_name'])
            self.send_chat_message(message)

            try:
                response = self.receive_chat_message()
                logger.info(f'Response: {response}')
            except Exception as e:
                logger.exception('Error receiving message: %s', e)

    def parse_response(self, response):
        if response['response'] == 200:
            return f"Server response: {response['alert']}"
        elif response['response'] == 400:
            return f"Server error: {response['error']}"
        else:
            return "Unknown response from server"
