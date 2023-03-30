import json

def receive_message(sock):
    encoded_response = sock.recv(4096)
    response = json.loads(encoded_response.decode('utf-8'))
    return response