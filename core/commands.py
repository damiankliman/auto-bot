import os
import random
import discord
from core import services
from core.models import CarType, Car
from table2ascii import table2ascii as t2a, PresetStyle
from datetime import datetime

def handle_commands(bot):
    COMMAND_PREFIX = os.getenv('COMMAND_PREFIX') or '!'

    # /hello || Greet the user
    @bot.command()
    async def hello(ctx):
        await ctx.send(f"Hi there {ctx.local_user.username}!")

    # /bank || Get the amount of money the user has in their bank account
    @bot.command()
    async def bank(ctx):
        money = services.get_user_money_by_id(ctx.local_user.id)
        embed=discord.Embed(
            title=ctx.local_user.username,
            description=datetime.today().strftime('%d/%m/%Y'),
            color=0x2ca3ed
        )
        embed.set_author(name="Bank statement")
        embed.add_field(name="Chequing:", value=f"${money:,}", inline=True)
        embed.add_field(name="Savings", value="$0", inline=True)
        embed.set_footer(text="Please do not retain this for your records")
        await ctx.send(embed=embed)

    # /roll || Roll a random number between 1 and 99 (or a custom number)
    @bot.command()
    async def roll(ctx, max: int = 99):
        if max < 1:
            return await ctx.send("Please enter a valid number larger than 0")

        await ctx.send(str(random.randint(1, max)))

    # /dealer || See all available base cars for purchase
    @bot.command()
    async def dealer(ctx):
        dealer_cars = services.get_all_cars()
        dealer_cars.sort(key=lambda car: car.price)
        cars_table_output = t2a(
            header=["Year", "Make", "Model", "Trim", "Type", "Power", "Weight", "Price", "Order code"],
            body=[[car.year, car.make, car.model, car.trim, car.type.value, f"{car.horsepower:,} HP", f"{car.weight:,} lb", f"${car.price:,}", car.order_code] for car in dealer_cars],
            style=PresetStyle.thin_compact,
            last_col_heading=True
        )
        await ctx.send(f"```Here's a list of cars you can buy \n{cars_table_output} \nUse the {COMMAND_PREFIX}buy <order code> command to buy a car```")

    # /buy || Buy a car from the dealer
    @bot.command()
    async def buy(ctx, order_code: str = None):
        if not order_code:
            return await ctx.send(f"Please provide an order code, like this: **{COMMAND_PREFIX}buy E30A**")

        dealer_car = services.get_car_by_order_code(order_code)

        if not dealer_car:
            return await ctx.send("That car does not exist!")

        for user_car in ctx.local_user.cars:
            if user_car.id == dealer_car.id:
                return await ctx.send("You already own this car!")

        if len(ctx.local_user.cars) >= 4:
                return await ctx.send("Your garage is already full! (max 4 cars)")

        if ctx.local_user.money < dealer_car.price:
            return await ctx.send("You do not have enough money to buy this car!")

        services.buy_car(ctx.local_user.id, dealer_car.id)
        await ctx.send(f"You bought a {dealer_car.year} {dealer_car.make} {dealer_car.model} {dealer_car.trim} for ${dealer_car.price:,}!")

    # /garage || See all cars in the user's garage
    @bot.command()
    async def garage(ctx):
        user_cars = ctx.local_user.cars
        cars_table_output = t2a(
            header=["Year", "Make", "Model", "Trim", "Type", "Power"],
            body=[[car.year, car.make, car.model, car.trim, car.type.value, f"{car.horsepower:,} HP"] for car in user_cars],
            style=PresetStyle.thin_compact,
            last_col_heading=True
        )
        await ctx.send(f"Here's your garage: \n```{cars_table_output}```")

    # /help || Get a list of all commands
    @bot.command()
    async def help(ctx):
        await ctx.send(
f"""
Here's a list of commands you can use:
```
{COMMAND_PREFIX}help - Get a list of commands
{COMMAND_PREFIX}hello - Say hi!
{COMMAND_PREFIX}bank - Check your bank account
{COMMAND_PREFIX}dealer - See all available cars for purchase
{COMMAND_PREFIX}buy <order code> - Buy a car from the dealer
{COMMAND_PREFIX}garage - See all cars in your garage
{COMMAND_PREFIX}roll <optional number> - Roll a random number between 1 and 99 (or a custom number)
```""")
