import os
import socket

from dotenv import load_dotenv


class Client:
    def __init__(self):
        self.socket = None
        print('Client is running, please, press ctrl+c to stop')

    def run(self):
        while True:
            print('>>>:')
            request = input()

            self.socket = socket.socket()
            self.send(request)
            response = self.listen()

            print(response)

    def send(self, data):
        try:
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            self.socket.send(bytearray(data, encoding='utf-8'))
        except ConnectionRefusedError:
            print('Exception: connection closed')
            exit()

    def listen(self):
        data = self.socket.recv(PACKAGE_SIZE).decode()
        self.socket.close()
        return data


load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
PACKAGE_SIZE = int(os.getenv("PACKAGE_SIZE"))
QUEUE_SIZE = int(os.getenv("QUEUE_SIZE"))

app = Client()

app.run()
