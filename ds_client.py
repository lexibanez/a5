# Starter code for assignment 5 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lex Ibanez
# laibanez@uci.edu
# 70063614

"""
This module contains functions to connect to a DS server and send messages.
The `send` function takes server details, user credentials, and
a message, and sends the message to the server.
"""


import socket
import json
import time
from ds_protocol import extract_json, extract_messages


def send(server: str, port: int, username: str,
         password: str, message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both
    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''

    response_tuple = join_server(server, port, username, password)

    # if username or password is taken, return False
    try:
        if response_tuple.type == 'error':
            print(response_tuple.message)
            return False
    except AttributeError:
        return False

    token = response_tuple.token

    if message:
        post = {
            "token": token,
            "post":  {
                "entry": message,
                "timestamp": time.time()
            }
        }

        post_string = json.dumps(post)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))

            send = client.makefile('w')
            recv = client.makefile('r')

            send.write(post_string + '\r\n')
            send.flush()

            resp = recv.readline()
            response_tuple = extract_json(resp)
            print(response_tuple.message)

    if bio:
        bio = {
            "token": token,
            "bio": {
                "entry": bio,
                "timestamp": time.time()
            }
        }

        bio_string = json.dumps(bio)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))

            send = client.makefile('w')
            recv = client.makefile('r')

            send.write(bio_string + '\r\n')
            send.flush()

            resp = recv.readline()
            response_tuple = extract_json(resp)
            if response_tuple.type == 'error':
                print(response_tuple.message)
                return False

    return True


def join_server(server, port, username, password):
    """
    This function creates a JSON string with the provided username
    and password, and then attempts to connect to the specified
    server and port. It sends the JSON string to the server and
    waits for a response.
    """
    data = {
            "join": {
                "username": username,
                "password": password,
                "token": ''
            }
        }
    # create json string with data
    json_string = json.dumps(data)

    # start client and join DSP server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))

            send = client.makefile('w')
            recv = client.makefile('r')

            send.write(json_string + '\r\n')
            send.flush()

            resp = recv.readline()
            # extract the server response into a named tuple
            response_tuple = extract_json(resp)
            print(response_tuple.message)

            return response_tuple

    except TimeoutError as e:
        print(e)
        print('Try a different IP or port')
        return False
    except socket.gaierror:
        print('Invalid IP address')
        return False

def direct_message(server, port, username, password, type = None, recipient = None, entry: str = None):

    response_tuple = join_server(server, port, username, password)

    try:
        if response_tuple.type == 'error':
            print(response_tuple.message)
            return False
    except AttributeError:
        return False

    token = response_tuple.token
    
    if entry:
        response_tuple = send_direct_message(server, port, token, recipient, entry)
        print(response_tuple.message)

    if type:
        message_request = {
            "token": token,
            "directmessage": type
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((server, port))

                send = client.makefile('w')
                recv = client.makefile('r')

                send.write(json.dumps(message_request) + '\r\n')
                send.flush()

                resp = recv.readline()
                response_tuple = extract_messages(resp)
                print(response_tuple.messages)

        except TimeoutError as e:
            print(e)
            print('Try a different IP or port')
            return False
        except socket.gaierror:
            print('Invalid IP address')
            return False
        

def send_direct_message(server, port, token, recipient, entry):
    direct_message = {
        "token": token,
        "directmessage": {
            "entry": entry,
            "recipient": recipient,
            "timestamp": time.time()
        }
    }
    direct_message_string = json.dumps(direct_message)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))

            send = client.makefile('w')
            recv = client.makefile('r')

            send.write(direct_message_string + '\r\n')
            send.flush()

            response = recv.readline()
            response_tuple = extract_json(response)

            return response_tuple
        
    except TimeoutError as e:
        print(e)
        print('Try a different IP or port')
        return False
    except socket.gaierror:
        print('Invalid IP address')
        return False
    