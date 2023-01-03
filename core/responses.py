import random
from core.services import get_user_money_by_id

def handle_response(message: str, local_user):
    command = message.lower()

    if command == 'bank':
        money = get_user_money_by_id(local_user.id)
        return f"You have ${money:n} in your bank account"

    if command == 'hello':
        return "Hi there!"

    if command.startswith('roll'):
        max = 99

        if len(message.split()) > 1:
            custom_max = message.split()[1]

            if custom_max.isdigit():
                max = int(custom_max)
            else:
                return "Please enter a valid number"

        return str(random.randint(1, max))

    if command == 'help':
        return "`This is a help message`"
