import json
import socket
import sys
from server_log_config import logger
from log_decorator import log


def send_response(sock, response):
    encoded_response = json.dumps(response).encode('utf-8')
    sock.send(encoded_response)
    logger.info(f'Sent response: {response}')


def receive_message(sock):
    encoded_message = sock.recv(4096)
    message = json.loads(encoded_message.decode('utf-8'))
    logger.info(f'Received message: {message}')
    return message


def handle_presence_message(message):
    response = {
        'response': 200,
        'time': message['time'],
        'alert': 'OK'
    }
    logger.info(f'Handled presence message: {message}')
    return response


@log
def main():
    server_address = sys.argv[sys.argv.index('-a') + 1] if '-a' in sys.argv else ''
    server_port = int(sys.argv[sys.argv.index('-p') + 1]) if '-p' in sys.argv else 7777

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((server_address, server_port))
        sock.listen(1)

        while True:
            conn, addr = sock.accept()
            with conn:
                message = receive_message(conn)
                if message['action'] == 'presence':
                    response = handle_presence_message(message)
                    send_response(conn, response)
