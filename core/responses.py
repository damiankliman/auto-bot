import random
from core.services import get_user_money_by_id

def handle_response(message: str, local_user):
    command = message.lower().split()[0]
    arguments = message.lower().split()[1:]

    # /hello || Greet the user
    if command == 'hello':
        return f"Hi there {local_user.username}!"

    # /bank || Get the amount of money the user has in their bank account
    if command == 'bank':
        money = get_user_money_by_id(local_user.id)
        return f"You have ${money:n} in your bank account"

    # /roll || Roll a random number between 1 and 99 (or a custom number)
    if command.startswith('roll'):
        max = 99
        custom_max = arguments[0] if arguments[0:] else None

        if custom_max:
            if custom_max.isdigit():
                return str(random.randint(1, int(custom_max)))
            else:
                return "Please enter a valid number"

        return str(random.randint(1, max))

    # /help || Get a list of commands
    if command == 'help':
        return """
Here's a list of commands:
```/help - Get a list of commands
/hello - Say hi!
/bank - Check your bank account
/roll <optional number> - Roll a random number between 1 and 99 (or a custom number)
```"""
