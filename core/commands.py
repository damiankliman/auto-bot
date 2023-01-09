import os
import random
import discord
from discord.ui import View
from core import services
from core.models import CarType, Car
from core import components
from table2ascii import table2ascii as t2a, PresetStyle
from datetime import datetime
import re
import asyncio

def handle_commands(bot):
    COMMAND_PREFIX = os.getenv('COMMAND_PREFIX') or '!'

    # hello || Greet the user
    @bot.command()
    async def hello(ctx):
        await ctx.send(f"Hi there {ctx.local_user.username}!")

    # bank || Get the amount of money the user has in their bank account
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

    # roll || Roll a random number between 1 and 99 (or a custom number)
    @bot.command()
    async def roll(ctx, max: int = 99):
        if max < 1:
            return await ctx.send("Please enter a valid number larger than 0")

        await ctx.send(str(random.randint(1, max)))

    # dealer || See all available base cars for purchase
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
        await ctx.send(f"```Here's a list of cars you can buy \n{cars_table_output} \nUse the {COMMAND_PREFIX}buy car <order code> command to buy a car```")

    # buy || Buy a car from the dealer
    @bot.command()
    async def buy(ctx, type: str = None, order_code: str = None):
        if not type:
            return await ctx.send(f"Please provide a type, like this: **{COMMAND_PREFIX}buy mod EX1**")
        if not order_code:
            return await ctx.send(f"Please provide an order code, like this: **{COMMAND_PREFIX}buy car E30A**")

        if type == "car":
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
            await ctx.send(
                f"You bought a {dealer_car.year} {dealer_car.make} {dealer_car.model} {dealer_car.trim} for ${dealer_car.price:,}!"
            )

        elif type == "mod":
            mod = services.get_mod_by_order_code(order_code)
            user = ctx.local_user
            user_car_view = View()

            if not mod:
                return await ctx.send("That mod does not exist!")

            if ctx.local_user.money < mod.price:
                return await ctx.send("You do not have enough money to buy this mod!")

            for index, car in enumerate(user.cars):
                user_car_view.add_item(components.CarButton(car=car, index=index + 1))

            initial_message = await ctx.send(
                f"{user.username}, select the car you want to mod",
                view=user_car_view,
            )

            try:
                user_interaction = await bot.wait_for(
                    "interaction",
                    timeout=30,
                    check=lambda interaction: interaction.user.id == ctx.author.id
                )
                user_selected_car = services.get_user_car_by_id(user.id, user_interaction.data["custom_id"])
                for user_car_mod in user_selected_car.mods:
                    if user_car_mod.id == mod.id:
                        return await initial_message.edit(
                            content=f"You already have this mod on your car...",
                            view=None
                        )
                    if user_car_mod.type == mod.type:
                        return await initial_message.edit(
                            content=f"You already have a {mod.type.value} mod on your car...",
                        )

                await user_interaction.response.edit_message(
                    content=f"Modding your car...",
                    view=None
                )
            except asyncio.TimeoutError:
                return await initial_message.edit(
                    content=f"{user.username} took too long to select a car...",
                    view=None
                )

            services.buy_mod(ctx.local_user.id, user_selected_car.id, mod.id)
            await initial_message.edit(
                content = f"You bought a {mod.name} for ${mod.price:,}!"
            )

    # garage || See all cars in the user's garage
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

    # mods || See all available mods for purchase
    @bot.command()
    async def mods(ctx):
        available_mods = services.get_all_mods()
        available_mods.sort(key=lambda mod: mod.price)
        cars_table_output = t2a(
            header=["Mod", "Power", "Price", "Order code"],
            body=[[mod.name, f"+{mod.power_add:,} HP", f"${mod.price:,}", mod.order_code] for mod in available_mods],
            style=PresetStyle.thin_compact,
            last_col_heading=True
        )
        await ctx.send(f"```Here's a list of mods you can buy \n{cars_table_output} \nUse the {COMMAND_PREFIX}buy mod <order code> command to buy a mod```")

    # race || Race another user
    @bot.command()
    async def race(ctx, opponent: str = None, wager: int = 0):
        if not opponent:
            return await ctx.send(f"Please @ another user to race with, like this: **{COMMAND_PREFIX}race @user**")

        if not opponent.startswith("<@") or not opponent.endswith(">"):
            return await ctx.send(f"That is not a valid opponent, make sure to tag them like this: **{COMMAND_PREFIX}race @user**")

        opponent_id = re.sub("[^0-9]", "", opponent)
        user = ctx.local_user
        opponent = services.get_user_by_id(opponent_id)
        user_car_view = View()
        opponent_car_view = View()

        if opponent_id == str(user.discord_id):
            return await ctx.send("You can't race yourself...")

        if not user.cars:
            return await ctx.send("You do not have any cars to race with...")

        if not opponent.cars:
            return await ctx.send("Your opponent does not have any cars to race with...")

        if user.money < wager:
            return await ctx.send("You do not have enough money for this race...")

        if opponent.money < wager:
            return await ctx.send("Your opponent does not have enough money for this race...")

        for index, car in enumerate(user.cars):
            user_car_view.add_item(components.CarButton(car=car, index=index + 1))

        for index, car in enumerate(opponent.cars):
            opponent_car_view.add_item(components.CarButton(car=car, index=index + 1))

        initial_message = await ctx.send(
            f"{user.username}, select a car to race with | ${wager:,} race",
            view=user_car_view,
        )

        try:
            user_interaction = await bot.wait_for(
                "interaction",
                timeout=30,
                check=lambda interaction: interaction.user.id == ctx.author.id
            )
            user_selected_car_id = user_interaction.data["custom_id"]
            await user_interaction.response.edit_message(
                content=f"{opponent.username}, select a car to race with | ${wager:,} race",
                view=opponent_car_view
            )
        except asyncio.TimeoutError:
            return await initial_message.edit(
                content=f"{user.username} took too long to select a car...",
                view=None
            )

        try:
            opponent_interaction = await bot.wait_for(
                "interaction",
                timeout=30,
                check=lambda interaction: interaction.user.id == opponent.discord_id
            )
            opponent_selected_car_id = opponent_interaction.data["custom_id"]
            await opponent_interaction.response.edit_message(content="Race is starting...", view=None)
        except asyncio.TimeoutError:
            return await initial_message.edit(
                content=f"{opponent.username} took too long to select a car...",
                view=None
            )

        winner = services.race_cars(user, opponent, user_selected_car_id, opponent_selected_car_id, wager)
        await initial_message.edit(content=f"{winner.username} won the race and ${wager:,}")

    # help || Get a list of all commands
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
{COMMAND_PREFIX}race <@user> <optional wager> - Race another user
{COMMAND_PREFIX}roll <optional number> - Roll a random number between 1 and 99 (or a custom number)
```""")
