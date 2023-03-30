import unittest
from unittest.mock import MagicMock
from lesson_3 import client


class TestClient(unittest.TestCase):
    def setUp(self):
        self.sock = MagicMock()
        self.test_message = {
            'action': 'test',
            'time': 123456.789,
            'user': {
                'account_name': 'test',
                'status': 'test'
            }
        }
        self.test_response = {
            'response': 200,
            'time': 123456.789,
            'alert': 'OK'
        }

    def test_create_presence_message(self):
        presence_message = client.create_presence_message()
        self.assertEqual(presence_message['action'], 'presence')
        self.assertEqual(presence_message['user']['account_name'], 'Guest')

    def test_send_message(self):
        client.send_message(self.sock, self.test_message)
        self.sock.send.assert_called_once_with(
            client.json.dumps(self.test_message).encode('utf-8')
        )

    def test_receive_message(self):
        self.sock.recv.return_value = client.json.dumps(self.test_response).encode('utf-8')
        response = client.receive_message(self.sock)
        self.assertEqual(response, self.test_response)

    def test_parse_response(self):
        self.assertEqual(client.parse_response({'response': 200}), 'OK')
        self.assertEqual(client.parse_response({'response': 400}), 'Bad Request')
        self.assertEqual(client.parse_response({'response': 401}), 'Unauthorized')
        self.assertEqual(client.parse_response({'response': 500}), 'Unknown Error')

