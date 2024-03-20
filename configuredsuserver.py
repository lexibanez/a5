from ds_messenger import *


def send_message():
    server = '168.235.86.101'
    username = 'ericqui'
    password = 'password'

    dm = DirectMessenger(server, username, password)

    status = dm.send('sending this to lexibanez44', 'lexibanez44')

    print(status)
    print('----------------------------')


def check_messages():
    server = '168.235.86.101'
    username = 'lexibanez44'
    password = 'passwordlol'
    dm = DirectMessenger(server, username, password)
    messages = dm.retrieve_new()
    print(messages)

if __name__ == '__main__':
    #send_message()
    check_messages()