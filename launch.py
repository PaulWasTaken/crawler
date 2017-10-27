import click
import os
import config

from cmd_client.base import CommandChoice
from config.log import get_logger, SIMPLE
from resource import getrusage, RUSAGE_SELF
from sql.creator import create_db
from timeit import default_timer
from workers.abstract_worker import AbstractWorker

logger = get_logger(__file__, SIMPLE)


@click.command()
@click.argument("fabric", required=True, type=CommandChoice(["load", "get"]))
@click.argument("url", required=True)
@click.option("--depth", default=1, type=int)
@click.option("-n", default=1, type=int)
@click.option("--timeout", default=30, type=int)
@click.option("--ssl", default=config.VERIFY_SSL, is_flag=True)
@click.option("--size", default=config.STORAGE_THRESHOLD, type=int)
def run(fabric, url, **kwargs):
    if not os.path.exists(str(config.DB)):
        logger.info("Database was not found. Creating...")
        create_db()
        logger.info("Empty database has been successfully created.")

    worker = fabric(url, **kwargs)

    if not isinstance(worker, AbstractWorker):
        logger.error("%s is not expected worker.")
        exit(-1)

    start_time = default_timer()
    worker.run()
    logger.info("ok, execution time: %.2f, peak memory usage: %s Mb" %
                (default_timer() - start_time,
                 getrusage(RUSAGE_SELF).ru_maxrss / 1000))


if __name__ == '__main__':
    run()
