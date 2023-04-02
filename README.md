# auto-bot

A simple discord bot based game that resembles a local car scene.
Buy cars and race your friends with simple chat commands!

[Add the current production bot to your server](https://discord.com/api/oauth2/authorize?client_id=1059807062592344114&permissions=534723950656&scope=bot)

## Getting Started

### Dependencies

* Python 3.9
* pipenv
* Docker
* A discord bot token (From https://discord.com/developers/applications)

### Setting up a local enviroment

* Pull the the main branch
* Install all dependecies with `pipenv install`
* Create a .env file with the following (or copy the .env.example)
```
DISCORD_BOT_TOKEN=
DATABASE_URL=postgresql://py_bot:postgres@localhost:5432/py_bot
DEFAULT_USER_MONEY=5000
COMMAND_PREFIX=!
RACE_VARIANCE=30
```

### Executing program

* Start a local database with `docker-compose up -d`
* Open a pipenv shell with `pipenv shell`
* If its your first time starting the bot, run 'make db_upgrade' to populate tables
* Start the bot with `make start` or `make dev` (for dev mode)

## License

This project is licensed under the GNU 3 License - see the LICENSE.md file for details

## Resources

* Discord developer portal: https://discord.com/developers/docs/intro
* Discord.py docs: https://discordpy.readthedocs.io/en/stable/
* Sqlalchemy docs: https://docs.sqlalchemy.org/en/14/
* Alembic docs: https://alembic.sqlalchemy.org/en/latest/
