import sys
import time
import pickle
import signal
import socket
import threading
from util import HEADERSIZE, data_packet, all_keys

class Client:
    def __init__(self, ip=None, port=9999) -> None:
        if not ip:
            self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.address = (self.ip, self.port)
        self.connect_server()
        self.running = True

    def connect_server(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect(self.address)


    def recieve_data(self, socket_connection):
        while self.running:
            full_message = b''
            new_message = True
            message_length = 0
            while True:
                message = socket_connection.recv(HEADERSIZE + 4)
                if new_message:
                    if message[:HEADERSIZE]:
                        message_length = int(message[:HEADERSIZE])
                new_message = False

                full_message += message
                if len(full_message) - HEADERSIZE == message_length:
                    print(pickle.loads(full_message[HEADERSIZE:]))
                    new_message = True
                    full_message = b""



    def run(self):
        try:
            while self.running:
                s_thread = threading.Thread(target=self.recieve_data, args=[self.socket_client])
                s_thread.start()
                d= data_packet
                for key in list(all_keys(d)):
                    d[key] = input(f"Enter value of  {key}: ")
                #time.sleep(1)
                #inp = input("Press enter send data : ")
                #d = data_packet
                self.send_data(self.socket_client,d)
        except Exception as error:
            print(f"ERROR : {error}")
        finally:
            self.close()
            
            
    def send_data(self, socket_connection, data):
        message = pickle.dumps(data)
        message = bytes(f"{len(message):<{HEADERSIZE}}", 'utf-8') + message
        socket_connection.send(message)
        print(f"Sent Data from client to  server {socket_connection.getpeername()}: {data}")
        
    def close(self):
        self.running = False

def signal_handler(signal, frame):
    sys.exit(0)
    
if __name__ == '__main__':

    signal.signal(signal.SIGINT, lambda signal, frame : signal_handler(signal, frame))
    print("Client Launched")
    client = Client()
    client.run()