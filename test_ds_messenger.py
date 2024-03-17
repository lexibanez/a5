import unittest
from ds_messenger import DirectMessenger, DirectMessage

# def test_direct_messenger():
#     server = '168.235.86.101'
#     username = 'lexibanez'
#     password = 'passwordlol'

#     dmessenger = DirectMessenger(server, username, password)
#     print(dmessenger.dsuserver, dmessenger.port, dmessenger.username, dmessenger.password)
#     dm = DirectMessage()
#     dm.create_message('lexibanez', 'hello this is a test')
#     status = dmessenger.send(dm.message, dm.recipient)
#     print(status)
#     print(dmessenger.retrieve_new())
#     print(dmessenger.retrieve_all())


# test_direct_messenger()

class TestDirectMessenger(unittest.TestCase):
    def test_direct_message(self):
        # Organize Phase
        recipient = 'lexibanez'
        message = 'test message'

        # Action Phase
        dm = DirectMessage()
        dm.create_message(recipient, message)

        # Assert Phase
        self.assertEqual(dm.recipient, recipient)
        self.assertEqual(dm.message, message)
        self.assertIsNotNone(dm.timestamp)

    def test_direct_messenger(self):
        # Organize Phase
        server = '168.235.86.101'
        username = 'lexibanez'
        password = 'passwordlol'
        recipient = 'lexibanez'
        message = 'test message'
        dmessenger = DirectMessenger(server, username, password)
        dm = DirectMessage()
        dm.create_message(recipient, message)

        # Action Phase
        result = dmessenger.send(recipient, dm.message)

        # Assert Phase
        self.assertTrue(result)
    
    def test_retrieve_new(self):
        # Organize Phase
        server = '168.235.86.101'
        username = 'lexibanez'
        password = 'passwordlol'
        dmessenger = DirectMessenger(server, username, password)

        # Action Phase
        result = dmessenger.retrieve_new()

        # Assert Phase
        self.assertIsInstance(result, list)

    def test_retrieve_all(self):
        # Organize Phase
        server = '168.235.86.101'
        username = 'lexibanez'
        password = 'passwordlol'
        dmessenger = DirectMessenger(server, username, password)

        #Action Phase
        result = dmessenger.retrieve_all()

        # Assert Phase
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main()