import click

from workers.extractor import Extractor
from workers.loader import Loader


class CommandChoice(click.Choice):
    def __init__(self, choices):
        super().__init__(choices)
        self.commands = {"load": Loader, "get": Extractor}

    def convert(self, value, param, ctx):
        if value in self.choices:
            return self.commands[value]
        self.fail('invalid choice: %s. (choose from %s)' %
                  (value, ', '.join(self.choices)), param, ctx)