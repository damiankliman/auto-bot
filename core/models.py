from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text
from core.database import Base
import uuid

class User(Base):
  __tablename__ = 'user'
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  discord_id = Column(String, nullable=False)
  username = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

