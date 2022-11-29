import sys
import time
import uuid
import pickle
import socket
import traceback
from threading import Thread
from util import HEADERSIZE

class Client:
    def __init__(self, ip=None, port=9999) -> None:
        if not ip:
            self.ip = 'sammflynn.ddns.net'
        self.port = port
        self.address = (self.ip, self.port)
        self.connect_server()
        self.connected = True
        self.running = True

        self.name = str(uuid.uuid4())[0:4]

    def connect_server(self):
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect(self.address)
            self.connected = True

        except ConnectionRefusedError:
            print("Server Down")
            self.connected = False

    def start(self):
        if self.connected:
            self.client_thread = Thread(target=self.recieve_data, args=[self.socket_client])
            self.client_thread.start()

    def run(self):
        try:
            while self.running and self.connected:
                inp = input("Press enter send data : ")
                self.send_data(self.socket_client, inp)
                if inp == "<DISCONNECT>":
                    self.close()
        except KeyboardInterrupt:
            self.running = False


    def recieve_data(self, socket_connection):

        full_message = b''
        new_message = True
        message_length = 0
        while self.running and self.connected:
            try:
                message = socket_connection.recv(HEADERSIZE * 2)
            except ConnectionAbortedError:
                print("Closing client.")
                self.close()

            except Exception as error:
                self.running = False
                traceback.print_exc()

            else:
                if new_message:
                    if message[:HEADERSIZE]:
                        message_length = int(message[:HEADERSIZE])
                new_message = False

                full_message += message
                if len(full_message) - HEADERSIZE == message_length:
                    recieved_data = pickle.loads(full_message[HEADERSIZE:])
                    self.process_message(recieved_data)
                    new_message = True
                    full_message = b""
                    message_length = 0

        self.close()

            
            
    def send_data(self, socket_connection, data):
        message = pickle.dumps(data)
        message = bytes(f"{len(message):<{HEADERSIZE}}", 'utf-8') + message
        try:
            socket_connection.send(message)
            # print(f"Sent Data from client to  server {socket_connection.getpeername()}: {data}")
        except Exception as error:
            print(error)
            print("Error while sending")

    def process_message(self, recieved_data):
        # print(f" Recieved_data {recieved_data} -> size : {round(sys.getsizeof(recieved_data)*1e-3, 2)} KB") # start processing command here
        print("Process")

    def close(self):
        self.running = False
        self.connected = False
        self.socket_client.close()


    
if __name__ == '__main__':
    print("Client Launched")
    client = Client()
    client.start()
    client.run()