import sys
import pickle
import signal
import socket
import threading
from util import HEADERSIZE, data_packet

class Server:
    def __init__(self, ip=None, port=9999) -> None:
        if not ip:
            self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port

        self.address = (self.ip, self.port)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind(self.address)
        self.clients = set()
        self.running = True

    def run(self):
        self.socket_server.listen()
        while self.running:
            socket_connection, address = self.socket_server.accept() 
            threading.Thread(target=self.handle_client, args=[socket_connection, address]).start()
            self.clients.add(socket_connection)
            print(f"Active Connections {threading.activeCount() - 1}")
            print("New client connected.")
            self.send_data(socket_connection, "Hello, I am server.")



    def handle_client(self, socket_connection, address):
        print(f"client address : {address}")
        connected = True
        while connected:
            full_message = b''
            new_message = True
            message_length = 0
            while self.running:
                message = socket_connection.recv(HEADERSIZE + 4)
                if new_message:
                    if message[:HEADERSIZE]:
                        message_length = int(message[:HEADERSIZE])
                    new_message = False
                full_message += message
                if len(full_message) - HEADERSIZE == message_length:
                    recieved_data = pickle.loads(full_message[HEADERSIZE:])
                    self.process_message(address, recieved_data)

                    if recieved_data == "<DISCONNECT>":
                        connected = False
                        socket_connection.close()
                    new_message = True
                    full_message = b""



    def send_data(self, client_socket, data):
        message = pickle.dumps(data)
        message = bytes(f"{len(message):<{HEADERSIZE}}", 'utf-8') + message
        client_socket.send(message)
        
        print(f"Sent Data from server to {client_socket.getpeername()}: {data}")
    
    def process_message(self, address, recieved_data):
        print(f"from : {address} -> data : {recieved_data} -> size : {round(sys.getsizeof(recieved_data)*1e-6, 2)} MB")
        
    def close(self):
        self.running = False

def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda signal, frame : signal_handler(signal, frame))
    print("Server Launched")
    server = Server()
    server.run()