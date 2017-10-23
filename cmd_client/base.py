import click

from loader import load_urls
from sql.extractor import extract_values


class CommandChoice(click.Choice):
    def __init__(self, choices):
        super().__init__(choices)
        self.commands = {"load": load_urls, "get": extract_values}

    def convert(self, value, param, ctx):
        if value in self.choices:
            return self.commands[value]
        self.fail('invalid choice: %s. (choose from %s)' %
                  (value, ', '.join(self.choices)), param, ctx)