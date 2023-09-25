from datetime import datetime

from server.exceptions import InvalidSyntaxException, CloseConnectionException


class TimeCommandMixin:
    def time_validate(self, data):
        if sum(1 for char in data if char.isalnum()) != 0:
            raise InvalidSyntaxException

    def time_command(self, data):
        self.time_validate(data)
        return str(datetime.now())


class EchoCommandMixin:
    def echo_validate(self, data):
        if sum(1 for char in data if char.isalnum()) == 0:
            raise InvalidSyntaxException

    def echo_command(self, data):
        self.echo_validate(data)
        return data


class CloseConnectionMixin:
    def close_validate(self, data):
        if sum(1 for char in data if char.isalnum()) != 0:
            raise InvalidSyntaxException

    def close_command(self, data):
        self.close_validate(data)
        raise CloseConnectionException
