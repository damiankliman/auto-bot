from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  discord_id = Column(String)
  username = Column(String)

  def __repr__(self):
    return "<User(discord_id='{}', username='{}')>"\
        .format(self.discord_id, self.username)
