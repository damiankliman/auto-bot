from sqlalchemy.orm import Session
from core.database import get_db
from core.models import User
import random

def get_all_users(db: Session = next(get_db())):
  users = db.query(User).first()
  return users

def handle_response(message):
  p_message = message.lower()

  if p_message == 'hello':
    return "Hi there!"

  if p_message.startswith('roll'):
    max = 99

    if len(message.split()) > 1:
      custom_max = message.split()[1]

      if custom_max.isdigit():
        max = int(custom_max)
      else:
        return "Please enter a valid number"

    return str(random.randint(1, max))

  if p_message == 'help':
    return "`This is a help message`"

  if p_message == 'users':
   return get_all_users().__dict__
