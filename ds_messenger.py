'''This module contains classes used in
the GUI module to send and retrieve'''
import time
from ds_client import direct_message
# pylint: disable=R0903

class DirectMessage:
    '''This class is used to
    create a message object.'''
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None

    def create_message(self, recipient, message):
        '''Create a message object.'''
        self.recipient = recipient
        self.message = message
        self.timestamp = time.time()


class DirectMessenger:
    '''This class is used to send and retrieve messages'''
    def __init__(self, dsuserver=None, username=None, password=None):
        '''initialize the DirectMessenger object'''
        self.token = None
        self.dsuserver = dsuserver
        self.port = 3021
        self.username = username
        self.password = password

    def send(self, message, recipient) -> bool:
        '''Send a message to the server'''
        # must return true if message successfully sent, false if send failed.
        response_tuple = direct_message(
            self.dsuserver,
            self.port,
            self.username,
            self.password,
            None,
            recipient,
            message
        )

        if response_tuple.type == 'error':
            return False

        return True

    def retrieve_new(self) -> list:
        '''Retrieve new messages from the server'''
        # must return a list of DirectMessage
        # objects containing all new messages
        messages_tuple = direct_message(
            self.dsuserver,
            self.port,
            self.username,
            self.password,
            'new'
        )
        return messages_tuple.messages

    def retrieve_all(self) -> list:
        '''Retrieve all messages from the server'''
        # must return a list of DirectMessage objects containing all messages
        messages_tuple = direct_message(
            self.dsuserver,
            self.port,
            self.username,
            self.password,
            'all'
        )
        return messages_tuple.messages
