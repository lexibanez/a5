'''This is a test module for the ds_protocol module.'''
import unittest
from ds_protocol import extract_json, extract_messages
from ds_client import direct_message
# pylint: disable=C0116

class TestDSProtocol(unittest.TestCase):
    '''This is a test class for the ds_protocol module.'''
    def test_direct_message(self):
        # Organize Phase
        server = '168.235.86.101'  # Replace with your server IP
        port = 3021  # Replace with server port
        username = 'lexibanez'
        password = 'passwordlol'
        type1 = 'all'
        type2 = 'new'

        # Action Phase
        result1 = direct_message(server, port, username, password, type1)
        result2 = direct_message(server, port, username, password, type2)

        # Assert Phase
        self.assertEqual(result1.type, 'ok')
        self.assertEqual(result2.type, 'ok')

    def test_send_direct_message(self):
        # Organize Phase
        server = '168.235.86.101'  # Replace with your server IP
        port = 3021  # Replace with server port
        username = 'lexibanez'
        password = 'passwordlol'
        recipient = 'lexibanez'
        entry = 'hello this is a test message'

        # Action Phase
        result = direct_message(server, port, username, password,
                                None, recipient, entry)

        # Assert Phase
        self.assertEqual(result.type, 'ok')

    def test_json_decode_error(self):
        # Organize Phase
        json_msg = 'this is not a json string'

        # Action Phase
        result = extract_json(json_msg)
        result2 = extract_messages(json_msg)

        # Assert Phase
        self.assertEqual(result, 'json cannot be decoded.')
        self.assertEqual(result2, 'json cannot be decoded.')


if __name__ == '__main__':
    unittest.main()
