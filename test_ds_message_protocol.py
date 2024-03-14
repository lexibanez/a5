from ds_protocol import *
from ds_client import *

def test_direct_message():
    server = '168.235.86.101'
    port = 3021

    test1 = direct_message(server, port, 'lexibanez', 'passwordlol', None, 'iguess', 'hello')

    test2 = direct_message(server, port, 'lexibanez', 'passwordlol', None, 'lexibanez', 'hello this is a test')

    test3 = direct_message(server, port, 'lexibanez', 'passwordlol', 'all')
    
    test4 = direct_message(server, port, 'lexibanez', 'passwordlol', 'new')

test_direct_message()

