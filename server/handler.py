import inspect
import re

from server.commands import EchoCommandMixin, TimeCommandMixin, CloseConnectionMixin
from server.exceptions import UnknownCommandException, WrongInputException


class CommandHandler(
    EchoCommandMixin,
    TimeCommandMixin,
    CloseConnectionMixin,
):

    def __init__(self):
        self.action = {}

        attributes = inspect.getmembers(CommandHandler)
        for method in attributes:
            if callable(method[1]) and method[0].endswith('_command'):
                pos = method[0].find("_command")
                name = method[0][:pos].upper()

                self.action[name] = method[1]

        print(f'Commands available: {self.action.keys()}')

    def handle(self, data):
        pattern = r'^\s*(\S+)\s*(.*)$'
        match = re.match(pattern, data)
        if not match:
            raise WrongInputException

        command = match.group(1).upper()
        extra_data = match.group(2)

        if command not in self.action.keys():
            raise UnknownCommandException

        data = self.action[command](self, extra_data)
        return data
