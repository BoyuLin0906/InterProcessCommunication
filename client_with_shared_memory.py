import time
from multiprocessing import shared_memory
from collections import Counter
from settings import SHARED_MEMORY_NAME

class SharedMemoryClient:
    def __init__(self, shared_memory_name):
        # Create shared memory
        self.shared_memory_client = shared_memory.ShareableList(sequence= [0]*4096, name=shared_memory_name)
        print("Client3 (shared memory) is ready")
    
    def run(self):
        # Receive data from host
        while self.shared_memory_client[0] == 0: time.sleep(1)
        # Parse data
        data = [0] * self.shared_memory_client[0]
        for idx in range(self.shared_memory_client[0]):
            data[idx] = self.shared_memory_client[idx+1]
        self.calculate_mode(data)

    def close(self):
        if self.shared_memory_client:
            self.shared_memory_client.shm.close()
            self.shared_memory_client.shm.unlink()
    
    def calculate_mode(self, data):
        if isinstance(data, list):
            # count numbers
            counter = Counter(data)
            most_common_list = counter.most_common()
            most_count = most_common_list[0][1]

            # find mode
            modes = list()
            for number, count in most_common_list:
                if count != most_count: break
                modes.append(str(number))
            if len(modes) > 1:
                mode_str = ', '.join(modes)
                print(f'Mode are {mode_str}')
            else:
                print(f'Mode is {modes[0]}')
        else:
            print("Input data needs to be list()")


if __name__ == '__main__':
    time.sleep(3)
    socket_client = SharedMemoryClient(SHARED_MEMORY_NAME)
    socket_client.run()
    socket_client.close()