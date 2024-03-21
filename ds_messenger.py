import time
from ds_client import *


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None

    def create_message(self, recipient, message):
        self.recipient = recipient
        self.message = message
        self.timestamp = time.time()


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.port = 3021
        self.username = username
        self.password = password

    def send(self, message, recipient) -> bool:
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
        # must return a list of DirectMessage objects containing all messages
        messages_tuple = direct_message(
            self.dsuserver,
            self.port,
            self.username,
            self.password,
            'all'
        )
        return messages_tuple.messages
