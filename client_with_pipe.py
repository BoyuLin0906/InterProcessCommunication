import time
import os
import sys
from settings import NAMED_PIPE

class PipeClient:
    def __init__(self, named_pipe):
        # Create pipe
        self.named_pipe = named_pipe
        timeout_count = 0
        while not os.path.exists(self.named_pipe) and timeout_count < 10:
            timeout_count += 1
            time.sleep(1)
        if timeout_count == 10: sys.exit()
        print("Client2 (pipe) is ready")
        
    def run(self):
        # Get data from pipe
        data = None
        with open(NAMED_PIPE, 'r') as fifo:
            data = fifo.read()
            if data:
                data = eval(data)
                self.calculate_median(data)
            fifo.close()
    
    def close(self):
        if os.path.exists(self.named_pipe): os.remove(self.named_pipe)
    
    def calculate_median(self, data):
        if isinstance(data, list):
            data_len = len(data)
            data.sort()
            median = 0
            if data_len % 2 == 1: median = data[data_len//2]
            else: median = (data[data_len//2] + data[(data_len//2)-1]) / 2
            print(f'Median is {median}')
        else:
            print("Input data needs to be list()")
    
    
if __name__ == '__main__':
    time.sleep(2)
    socket_client = PipeClient(NAMED_PIPE)
    socket_client.run()
    socket_client.close()