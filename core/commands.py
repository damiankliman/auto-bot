import random
from core.services import get_user_money_by_id

def handle_commands(bot):

    # /hello || Greet the user
    @bot.command()
    async def hello(ctx):
        await ctx.send(f"Hi there {ctx.local_user.username}!")

    # /bank || Get the amount of money the user has in their bank account
    @bot.command()
    async def bank(ctx):
        money = get_user_money_by_id(ctx.local_user.id)
        await ctx.send(f"You have ${money:n} in your bank account")

    # /roll || Roll a random number between 1 and 99 (or a custom number)
    @bot.command()
    async def roll(ctx, max: int = 99):
        if max < 1:
            return await ctx.send("Please enter a valid number larger than 0")

        await ctx.send(str(random.randint(1, max)))
