from sqlalchemy import Column, Integer, String, Date
from core.database import Base

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True, nullable=False)
  discord_id = Column(String, nullable=False)
  username = Column(String, nullable=False)
  created_at = Column(Date, nullable=False)

  def __repr__(self):
    return "<User(discord_id='{}', username='{}')>"\
        .format(self.discord_id, self.username)
