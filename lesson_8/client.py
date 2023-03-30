import sys
import socket
import json
from send_message import send_message
from receive_message import receive_message
from log_decorator import log
from client_log_config import logger


def parse_response(response):
    if response['response'] == 200:
        return f"Server response: {response['alert']}"
    elif response['response'] == 400:
        return f"Server error: {response['error']}"
    else:
        return "Unknown response from server"


def create_presence_message(account_name='Guest'):
    message = {
        'action': 'presence',
        'time': 123456.789,
        'user': {
            'account_name': account_name,
            'status': 'Online'
        }
    }
    return message


def create_p2p_message(to, message_text, from_user):
    message = {
        'action': 'msg',
        'time': 123456.789,
        'to': to,
        'from': from_user,
        'message': message_text
    }
    return message


@log
def send_chat_message(sock, message):
    encoded_message = json.dumps(message).encode('utf-8')
    sock.send(encoded_message)


@log
def receive_chat_message(sock):
    encoded_message = sock.recv(4096)
    message = json.loads(encoded_message.decode('utf-8'))
    return message


@log
def main():
    server_address = sys.argv[1]
    server_port = int(sys.argv[2]) if len(sys.argv) > 2 else 7777

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_address, server_port))

        presence_message = create_presence_message()
        send_message(sock, presence_message)

        try:
            response = receive_message(sock)
        except Exception as e:
            logger.exception('Error receiving message: %s', e)
        logger.info(f'Response: {parse_response(response)}')

        while True:
            chat_message = input('Enter your message: ')
            to_user = input('Enter recipient name: ')
            message = create_p2p_message(to_user, chat_message, presence_message['user']['account_name'])
            send_chat_message(sock, message)

            try:
                response = receive_chat_message(sock)
                logger.info(f'Response: {response}')
            except Exception as e:
                logger.exception('Error receiving message: %s', e)


if __name__ == '__main__':
    main()
