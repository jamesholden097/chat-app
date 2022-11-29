import sys
import pickle
import signal
import socket
import threading
import traceback
from dataclasses import dataclass
from util import HEADERSIZE, data_packet

class User:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.name = ''

class Server:
    def __init__(self, ip='0.0.0.0', port=9999) -> None:
        #if not ip:
        self.ip = ip #socket.gethostbyname(socket.gethostname())
        self.port = port

        self.address = (self.ip, self.port)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # try except else finally
        self.socket_server.bind(self.address) # try except else finally
        self.clients = set()
        self.users = {}
        self.running = True

    def start(self):
        self.server_thread = threading.Thread(target=self.run, args=[])
        self.server_thread.start()

    def run(self):
        self.socket_server.listen()
        while self.running:
            socket_connection, address = self.socket_server.accept()  # try except else finally
            threading.Thread(target=self.handle_client, args=[socket_connection, address]).start()
            user = User(socket_connection, address)
            self.clients.add(user)
            # self.send_data(user.socket, "<REGISTER>")
            # print(f"Active Connections {threading.activeCount() - 1}")
            # print(len(self.clients))
            # print(self.clients)
            # self.send_data(socket_connection, "Hello, I am server.")



    def handle_client(self, socket_connection, address):
        # print(f"client socket_connection : {socket_connection}")
        print(f"client address : {address}")
        connected = True
        full_message = b''
        new_message = True
        message_length = 0
        while self.running and connected:
            try:
                message = socket_connection.recv(HEADERSIZE * 2)

            except ConnectionResetError:
                print(f"client diconnected")
                connected = False
                break # just for now

            #except Exception as error:
            #    print("Exception")
            #    traceback.print_exc()
            #    break # just for now

            else:
                if new_message:
                    if message[:HEADERSIZE]:
                        message_length = int(message[:HEADERSIZE])
                    new_message = False
                full_message += message
                if len(full_message) - HEADERSIZE == message_length:
                    recieved_data = pickle.loads(full_message[HEADERSIZE:])
                    self.send_data(socket_connection, recieved_data)

                    self.process_message(address, recieved_data)
                    new_message = True
                    full_message = b""
                    if recieved_data == "<DISCONNECT>":
                        print(f"Disconnect Request from client {socket_connection}")
                        connected = False
        self.clients.remove(socket_connection)
        socket_connection.close()


    def send_data(self, client_socket, data):
        message = pickle.dumps(data)
        message = bytes(f"{len(message):<{HEADERSIZE}}", 'utf-8') + message
        try:
            client_socket.send(message)
            # print(f"Sent Data from client to  server {socket_connection.getpeername()}: {data}")
        except Exception as error:
            print(error)
            print("Error while sending")
    
    def process_message(self, address, recieved_data):
        # print(f"from : {address} -> data : {recieved_data} -> size : {round(sys.getsizeof(recieved_data)*1e-3, 2)} KB") # start processing commands here
        print(f"from : {address} -> data : {recieved_data} -> size : {round(sys.getsizeof(recieved_data)*1e-3, 2)} KB") # start processing commands here
        
    def close(self):
        self.running = False

def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda signal, frame : signal_handler(signal, frame))
    print("Server Launched")
    server = Server()
    # server = Server(ip='103.88.142.105', port=9999)
    # server = Server(ip='192.168.1.110', port=9999)
    server.start()
    server.server_thread.join()