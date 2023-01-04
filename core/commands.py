import random
from core import services
from table2ascii import table2ascii as t2a, PresetStyle

def handle_commands(bot):

    # /hello || Greet the user
    @bot.command()
    async def hello(ctx):
        await ctx.send(f"Hi there {ctx.local_user.username}!")

    # /bank || Get the amount of money the user has in their bank account
    @bot.command()
    async def bank(ctx):
        money = services.get_user_money_by_id(ctx.local_user.id)
        await ctx.send(f"You have ${money:n} in your bank account")

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
            header=["Year", "Make", "Model", "Trim", "Type", "Price"],
            body=[[car.year, car.make, car.model, car.trim, car.type, car.price] for car in dealer_cars],
            style=PresetStyle.thin_compact
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
/roll <optional number> - Roll a random number between 1 and 99 (or a custom number)
```""")
