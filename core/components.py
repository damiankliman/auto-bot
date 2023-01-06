import discord
from discord.ui import Button

class CarButton(Button):
    def __init__(self, car, index):
        super().__init__(
            label=f"{car.year} {car.make} {car.model} {car.trim} | {car.horsepower} HP",
            style=discord.ButtonStyle.primary,
            custom_id=str(car.id),
            row=index,
        )
