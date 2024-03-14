from ds_messenger import DirectMessenger, DirectMessage

def test_direct_messenger():
    server = '168.235.86.101'
    username = 'lexibanez'
    password = 'passwordlol'

    dmessenger = DirectMessenger(server, username, password)
    print(dmessenger.dsuserver, dmessenger.port, dmessenger.username, dmessenger.password)
    dm = DirectMessage()
    dm.create_message('lexibanez', 'hello this is a test')
    status = dmessenger.send(dm.message, dm.recipient)
    print(status)
    print(dmessenger.retrieve_new())
    print(dmessenger.retrieve_all())


test_direct_messenger()