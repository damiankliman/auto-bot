from sqlalchemy.orm import Session
from core.database import get_db
from core.models import User
import os

def get_user_by_id(discord_id: int, db: Session = next(get_db())):
    return db.query(User).filter(User.discord_id == discord_id).one_or_none()

def create_user(discord_id: int, username: str, db: Session = next(get_db())):
    default_money = int(os.getenv('DEFAULT_USER_MONEY')) or 1000
    user = User(discord_id=discord_id, username=username, money=default_money)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_or_create_local_user(author):
    user = get_user_by_id(author.id)

    if user:
        print(f"Found user for {author.name}")

    if not user:
        print(f"Creating new user for {author.name}")
        user = create_user(author.id, author.name)

    return user

def get_user_money_by_id(user_id, db: Session = next(get_db())):
    user = db.query(User).filter(User.id == user_id).one_or_none()
    return user.money
