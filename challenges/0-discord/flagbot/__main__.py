import argparse
import logging

import discord

from . import config
from . import fakeshell

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info('Ready!')
        logging.info(f'Logged on as {self.user}')

        game = discord.Game("Capture the Flag")
        await self.change_presence(activity=game)

    async def on_message(self, message):
        if message.author == self.user:
            # ignore messages from self
            return
        if message.guild:
            # only reply in private messages
            return

        result = fakeshell.run(message.content)
        logging.info(f"running \"{message.content}\" from {message.author}")
        await message.author.send(f"```\n{result}\n```")

LOG_LEVELS = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", choices=LOG_LEVELS.keys(), default="info")
    args = parser.parse_args()

    logging.basicConfig(level=LOG_LEVELS[args.log])

    client = MyClient()
    client.run(config.TOKEN)

if __name__ == "__main__":
    main()
