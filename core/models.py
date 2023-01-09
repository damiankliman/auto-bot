from sqlalchemy import Column, String, BigInteger, Integer, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text
from core.database import Base
import uuid
import enum

class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    discord_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    money = Column(BigInteger, nullable=True)
    cars = relationship('Car', secondary='user_car', back_populates='users', lazy='joined')

class CarType(enum.Enum):
    HATCHBACK = 'Hatchback'
    COUPE = 'Coupe'
    PICKUP = 'Pickup'
    SEDAN = 'Sedan'
    STATION_WAGON = 'Station Wagon'

CarTypeType: Enum = Enum(
    CarType,
    name="car_type_type",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)

class Car(Base):
    __tablename__ = 'car'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    trim = Column(String, nullable=False)
    type = Column(Enum(CarType), nullable=False)
    horsepower = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    order_code = Column(String, unique=True, nullable=False)
    factory_induction = Column(Boolean, nullable=True)
    users = relationship('User', secondary='user_car', back_populates='cars')

class UserCar(Base):
    __tablename__ = 'user_car'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    car_id = Column(UUID(as_uuid=True), ForeignKey('car.id'))
    mods = relationship('Mod', secondary='user_car_mod', back_populates='user_cars', lazy='joined')

class ModType(enum.Enum):
    INDUCTION = 'induction'
    INTERCOOLER = 'intercooler'
    INTAKE = 'intake'
    ENGINE = 'engine'
    RADIATOR = 'radiator'
    SUSPENSION = 'suspension'
    EXHAUST = 'exhaust'

ModTypeType: Enum = Enum(
    ModType,
    name="mod_type_type",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)

class Mod(Base):
    __tablename__ = 'mod'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(ModType), nullable=False)
    price = Column(Integer, nullable=False)
    power_add = Column(Integer, nullable=False)
    order_code = Column(String, unique=True, nullable=False)
    user_cars = relationship('UserCar', secondary='user_car_mod', back_populates='mods')

class UserCarMod(Base):
    __tablename__ = 'user_car_mod'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_car_id = Column(UUID(as_uuid=True), ForeignKey('user_car.id'))
    mod_id = Column(UUID(as_uuid=True), ForeignKey('mod.id'))
