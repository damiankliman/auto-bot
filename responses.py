import random

def handle_response(message):
  p_message = message.lower()
  
  if p_message == 'hello':
    return "Hi there!"
  
  if p_message == 'roll':
    return str(random.randint(1, 99))
  
  if p_message == '!help':
    return "`This is a help message`"
  