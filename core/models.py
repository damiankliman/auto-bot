from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text
from core.database import Base
import uuid

class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    discord_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    money = Column(BigInteger, nullable=True)

class Car(Base):
    __tablename__ = 'car'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    trim = Column(String, nullable=False)
    type = Column(String, nullable=False)
    horsepower = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
