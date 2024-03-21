"""
This module contains functions to handle the DSP protocol.
The `extract_json` function takes a JSON message string, parses it,
and returns a namedtuple with the extracted information.
"""
# ds_protocol.py

# Starter code for assignment 5 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lex Ibanez
# laibanez@uci.edu
# 70063614


import json
from collections import namedtuple


Response = namedtuple('Response', ['type', 'message', 'token'],
                      defaults=[None, None, None])

Messages = namedtuple('Messages', ['type', 'messages'],
                      defaults=[None, None])


def extract_json(json_msg: str) -> Response:
    '''
    Call the json.loads function on a json string
    and convert it to a DataTuple object
    '''
    try:
        message_dict = json.loads(json_msg)
        msg_type = message_dict['response']['type']
        message = message_dict['response']['message']
        token = message_dict['response'].get('token')
        return Response(msg_type, message, token)

    except json.JSONDecodeError:
        return 'json cannot be decoded.'


def extract_messages(json_msg: str):
    '''Call the json.loads function on a json string
    and convert it to a DataTuple object'''

    try:
        message_dict = json.loads(json_msg)
        msg_type = message_dict['response']['type']
        messages = message_dict['response']['messages']
        return Messages(msg_type, messages)

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return 'json cannot be decoded.'
