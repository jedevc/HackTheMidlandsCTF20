import logging

import discord

from . import fakeshell

class FlagBotClient(discord.Client):
    async def on_ready(self):
        logging.info('Ready!')
        logging.info(f'Logged on as {self.user}')

        game = discord.Game("Capture the Flag in DMs")
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
