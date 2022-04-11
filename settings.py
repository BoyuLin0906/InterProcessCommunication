import os

# Start clients automatically
AUTO_CLIENTS = True
# Socket
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 6001
# Shared Memory
SHARED_MEMORY_NAME = 'MY_SHM'
# PIPE
PIPE_TMP_DIR = '/tmp'
NAMED_PIPE = os.path.join(PIPE_TMP_DIR, 'MY_PIPE')
