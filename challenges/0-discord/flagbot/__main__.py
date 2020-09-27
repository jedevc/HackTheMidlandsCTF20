import argparse
import logging

import discord

from . import config
from .flagbot import FlagBotClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", choices=LOG_LEVELS.keys(), default="info")
    args = parser.parse_args()

    logging.basicConfig(level=LOG_LEVELS[args.log])

    client = FlagBotClient()
    client.run(config.TOKEN)

LOG_LEVELS = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}

if __name__ == "__main__":
    main()
