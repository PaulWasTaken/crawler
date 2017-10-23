import sys
sys.path.append("/home/paul/Рабочий стол/pressindex_test")

import click
import os
import config

from asyncio import get_event_loop
from cmd_client.base import CommandChoice
from config.log import get_logger
from sql.creator import create
from utils import exception_handler
logger = get_logger(__file__)


@click.command()
@click.argument("command", required=True, type=CommandChoice(["load", "get"]))
@click.argument("url", required=True)
@click.option("--depth", default=1)
@click.option("-n", default=1)
@click.option("--timeout", default=10)
def run(command, url, **kwargs):
    if not os.path.exists(str(config.DB)):
        logger.debug("Database was not found. Creating...")
        create()
        logger.debug("Empty database has been successfully created.")

    loop = get_event_loop()
    loop.set_exception_handler(exception_handler)
    try:
        loop.run_until_complete(command([url], **kwargs))
    except KeyboardInterrupt:
        loop.stop()
        loop.close()


if __name__ == '__main__':
    run()
