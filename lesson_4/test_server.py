import unittest
from unittest.mock import MagicMock
from lesson_3 import server


class TestServer(unittest.TestCase):
    def setUp(self):
        self.sock = MagicMock()

    def test_handle_presence_message(self):
        presence_message = {
            'action': 'presence',
            'time': 123456.789,
            'user': {
                'account_name': 'test',
                'status': 'test'
            }
        }
        response = server.handle_presence_message(presence_message)
        self.assertEqual(response['response'], 200)
        self.assertEqual(response['time'], presence_message['time'])
        self.assertEqual(response['alert'], 'OK')