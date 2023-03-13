import json
import socket
import sys


def send_message(sock, message):
    encoded_message = json.dumps(message).encode('utf-8')
    sock.send(encoded_message)


def receive_message(sock):
    encoded_response = sock.recv(4096)
    response = json.loads(encoded_response.decode('utf-8'))
    return response


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


def parse_response(response):
    code = response.get('response')
    if code == 200:
        return 'OK'
    elif code == 400:
        return 'Bad Request'
    elif code == 401:
        return 'Unauthorized'
    else:
        return 'Unknown Error'


if __name__ == '__main__':
    server_address = sys.argv[1]
    server_port = int(sys.argv[2]) if len(sys.argv) > 2 else 7777

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_address, server_port))

        presence_message = create_presence_message()
        send_message(sock, presence_message)

        response = receive_message(sock)
        print(parse_response(response))
