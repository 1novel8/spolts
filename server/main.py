import socket
import os

from dotenv import load_dotenv

from server.handler import CommandHandler
from server.exceptions import (WrongInputException,
                               UnknownCommandException,
                               InvalidSyntaxException,
                               CloseConnectionException)


load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
PACKAGE_SIZE = int(os.getenv("PACKAGE_SIZE"))
QUEUE_SIZE = int(os.getenv("QUEUE_SIZE"))


class Server:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('', SERVER_PORT))
        self.socket.listen(QUEUE_SIZE)
        self.commander = CommandHandler()

    def run(self):
        while True:
            conn, request = self.listen()
            try:
                response = self.commander.handle(request)
                self.send(conn, response)
            except WrongInputException:
                self.send(conn, 'EXCEPTION: Wrong Input!')
            except UnknownCommandException:
                self.send(conn, 'EXCEPTION: Unknown command!')
            except InvalidSyntaxException:
                self.send(conn, 'EXCEPTION: Invalid syntax!')
            except CloseConnectionException:
                self.socket.close()
                exit()

    def listen(self):
        conn, addr = self.socket.accept()
        print(f'connected to: {addr}')
        data = conn.recv(PACKAGE_SIZE).decode()
        return conn, data

    def send(self, conn, data: str):
        conn.send(data.encode("utf-8"))
        conn.close()


app = Server()

app.run()
