import socket
import pickle
import time
import re
import os
import subprocess
import signal
from multiprocessing import shared_memory
from settings import SOCKET_HOST, SOCKET_PORT, SHARED_MEMORY_NAME, NAMED_PIPE


class SocketServer:
    def __init__(self, socket_host, socket_port):
        # Create socket server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket_host, socket_port))
        server.listen(5)
        self.connection, _ = server.accept()
    
    def run(self, data):
        if self.connection:
            # Send data to client
            data = pickle.dumps(data)
            self.connection.send(data)
            
            # Receive response from client
            data = self.connection.recv(1024)
            data = pickle.loads(data)
            if not data: print("Failed to calculate the MEAN")
    
    def close(self):
        if self.connection: self.connection.close()


class SharedMemoryHost:
    def __init__(self, shared_memory_name):
        # Create shared memory
        self.shared_memory = shared_memory.ShareableList(name=shared_memory_name)
        
    def run(self, data):
        # Save data in shared memory
        if self.shared_memory:
            for idx in range(len(data)):
                self.shared_memory[idx] = data[idx]
        
    def close(self):
        if self.shared_memory:
            self.shared_memory.shm.close()


class PipeHost:
    def __init__(self, named_pipe):
        # Create pipe
        self.named_pipe = named_pipe
        if not os.path.exists(named_pipe): os.mkfifo(named_pipe, 0o777)

    def run(self, data):
        # Send data to pipe
        with open(self.named_pipe, 'w') as fifo:
            print(str(data), file=fifo)
            fifo.close()


def parse_data(data):
    for idx in range(len(data)):
        if re.match("[-+]?\d+$", data[idx]): data[idx] = int(data[idx])
        else:
            print("The data contains non-integer numbers")
            return False
    return True


def kill_clients(*arg):
    files = [file for file in os.listdir('.') if os.path.isfile(file) and 'client' in os.path.splitext(file)[0]]
    process = subprocess.Popen(['ps', '-ax'], stdout=subprocess.PIPE)
    out, _ = process.communicate()
    for line in out.splitlines():
        for file in files:
            if file in str(line):
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)


if __name__ == '__main__':
    # Handle ctrl + c
    signal.signal(signal.SIGINT, kill_clients)
    
    # Create Server
    socket_server = SocketServer(SOCKET_HOST, SOCKET_PORT)
    pipe_host = PipeHost(NAMED_PIPE)
    time.sleep(4)
    shared_memory_host = SharedMemoryHost(SHARED_MEMORY_NAME)
    
    # Input data by typing
    input_message = "Server is ready. You can type intergers and then click [ENTER].\
                    \nClients will show the mean, median, and mode of the input values:\n"
    data = input(input_message)
    data = data.strip().split()
    parsed_status = parse_data(data)
    
    # Send data to clients
    if parsed_status and data:
        socket_server.run(data)
        pipe_host.run(data)
        shared_memory_host.run([len(data)] + data)
    else:
        print("Input error")
        kill_clients()
        
    time.sleep(1)
    socket_server.close()
    shared_memory_host.close()