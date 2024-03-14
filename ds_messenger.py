from ds_client import direct_message

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
		
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    response_tuple = direct_message(self.dsuserver, self.username, self.password, None, recipient, message)
    if response_tuple.type == 'error':
      return False
    
    return True
		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    messages_tuple = direct_message(self.dsuserver, self.username, self.password, 'new')
    return messages_tuple.messages
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    messages_tuple = direct_message(self.dsuserver, self.username, self.password, 'all')
    return messages_tuple.messages