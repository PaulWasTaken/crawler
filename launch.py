import sys
sys.path.append("/home/paul/Рабочий стол/pressindex_test")

import click
import os
import config

from cmd_client.base import CommandChoice
from config.log import get_logger
from sql.creator import create
from workers.abstract_worker import AbstractWorker
logger = get_logger(__file__)


@click.command()
@click.argument("fabric", required=True, type=CommandChoice(["load", "get"]))
@click.argument("url", required=True)
@click.option("--depth", default=1)
@click.option("-n", default=1)
@click.option("--timeout", default=90)
def run(fabric, url, **kwargs):
    if not os.path.exists(str(config.DB)):
        logger.debug("Database was not found. Creating...")
        create()
        logger.debug("Empty database has been successfully created.")

    worker = fabric(url, **kwargs)

    if not isinstance(worker, AbstractWorker):
        logger.error("%s is not expected worker.")

    worker.run()


if __name__ == '__main__':
    run()
