import socket
import time
import pickle
from settings import SOCKET_HOST, SOCKET_PORT

class SocketClient:
    def __init__(self, socket_host, socket_port):
        # Create client
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((socket_host, socket_port))
        print("Client1 (socket) is ready")
    
    def run(self):
        # Receive data from server
        data = self.socket_client.recv(1024)
        
        # Parse data and calculate mean
        status = False
        if data:
            data = pickle.loads(data)
            status = self.calculate_mean(data)
        
        # Return the status to server
        resp_data = pickle.dumps(status)
        self.socket_client.send(resp_data)
    
    def close(self):
        # Close client
        self.socket_client.close()
    
    def calculate_mean(self, data):
        if data and isinstance(data, list):
            mean = round(sum(data) / len(data), 5)
            print(f'Mean is {mean}')
            return True
        else:
            print("Input data needs to be list()")
            return False


if __name__ == '__main__':
    time.sleep(1)
    socket_client = SocketClient(SOCKET_HOST, SOCKET_PORT)
    socket_client.run()
    socket_client.close()