from sqlalchemy.orm import Session
from core.database import get_db
from core.models import User

def get_user_by_id(discord_id: int, db: Session = next(get_db())):
    return db.query(User).filter(User.discord_id == discord_id).one_or_none()

def create_user(discord_id: int, username: str, db: Session = next(get_db())):
    user = User(discord_id=discord_id, username=username)
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
