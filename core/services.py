from sqlalchemy.orm import Session
from core.database import get_db
from core.models import User, Car
import os
import random

def get_user_by_id(discord_id: int, db: Session = next(get_db())):
    user = db.query(User).filter(User.discord_id == discord_id).one_or_none()
    db.close()
    return user

def create_user(discord_id: int, username: str, db: Session = next(get_db())):
    default_money = int(os.getenv('DEFAULT_USER_MONEY')) or 1000
    user = User(discord_id=discord_id, username=username, money=default_money)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
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
    db.close()
    return user.money

def get_all_cars(db: Session = next(get_db())):
    cars = db.query(Car).all()
    db.close()
    return cars

def get_car_by_order_code(order_code: str, db: Session = next(get_db())):
    car = db.query(Car).filter(Car.order_code == order_code).one_or_none()
    db.close()
    return car

def buy_car(user_id: str, car_id: str, db: Session = next(get_db())):
    user = db.query(User).filter(User.id == user_id).one_or_none()
    car = db.query(Car).filter(Car.id == car_id).one_or_none()
    user.money -= car.price
    user.cars.append(car)
    db.commit()
    db.close()
    return True

def race_cars(local_user, local_opponent, user_car_id, opponent_car_id, wager: int, db: Session = next(get_db())):
    user_car = db.query(Car).filter(Car.id == user_car_id).one_or_none()
    opponent_car = db.query(Car).filter(Car.id == opponent_car_id).one_or_none()
    user = db.query(User).filter(User.id == local_user.id).one_or_none()
    opponent = db.query(User).filter(User.id == local_opponent.id).one_or_none()

    variance = int(os.getenv('RACE_VARIANCE')) or 30
    user_power_weight_ratio = user_car.horsepower / user_car.weight
    opponent_power_weight_ratio = opponent_car.horsepower / opponent_car.weight
    user_luck = random.randint(50-variance/2, 50+variance/2)
    opponent_luck = random.randint(50-variance/2, 50+variance/2)

    user_result = user_power_weight_ratio * user_luck
    opponent_result = opponent_power_weight_ratio * opponent_luck

    if user_result > opponent_result:
        winner = user
    else:
        winner = opponent

    if wager > 0:
        if winner == user:
            user.money += wager
            opponent.money -= wager
        else:
            user.money -= wager
            opponent.money += wager

    db.commit()
    db.refresh(user)
    db.refresh(opponent)
    db.close()

    return winner



