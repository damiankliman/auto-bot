import random
import discord
from core import services
from core.models import CarType
from table2ascii import table2ascii as t2a, PresetStyle
from datetime import datetime

def handle_commands(bot):

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
        cars_table_output = t2a(
            header=["Year", "Make", "Model", "Trim", "Type", "Price", "Order code"],
            body=[[car.year, car.make, car.model, car.trim, CarType[car.type.name].value, f"${car.price:,}", car.order_code] for car in dealer_cars],
            style=PresetStyle.thin_compact,
            last_col_heading=True
        )
        await ctx.send(f"Here's a list of cars you can buy: \n```{cars_table_output}```")

    # /help || Get a list of all commands
    @bot.command()
    async def help(ctx):
        await ctx.send(
"""
Here's a list of commands you can use:
```
/help - Get a list of commands
/hello - Say hi!
/bank - Check your bank account
/dealer - See all available cars for purchase
/roll <optional number> - Roll a random number between 1 and 99 (or a custom number)
```""")
