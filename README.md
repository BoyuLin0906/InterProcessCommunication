# Inter-Process Communication

## Description

Create a program that uses 4 processes as follows. The Server process will monitor keyboard input from the user, and send the data to all client processes.

### Server (server.py)
    Accept user keyboard input. The user types integers and separate them by using [Space]. After clicking [Enter], server will write data to each clients via a socket, pipe, or the shared memory, respectively.

### Client1 (client_with_socket.py)
    Reads integers from the socket and calculate the Mean value of the integers.

### Client2 (client_with_pipe.py)
    Reads integers from the pipe and calculate the Median value of the integers.

### Client3 (client_with_shared_memory.py)
    Reads integers from the shared memory, and then calculating the Mode value of the integers.

<hr>

## Environment

- Operation System: Ubuntu 20.04.4 LTS
- Programming Language: Python 3.8.10

<hr>

## Get Started

1. Clone this github repository.

2. Run the command as follows:
    ```bash
    python3 client_with_socket.py & python3 client_with_shared_memory.py & python3 client_with_pipe.py & python3 server.py
    ```

3. Type the integers and press `Enter`:
    ```bash
    123 123 456 789
    ```

4. Finally, show the results from clients:
    ```bash
    Mean is 372.75
    Median is 289.5
    Mode is 123
    ```

5. Example:
    ```bash
    Client1 (socket) is ready
    Client2 (pipe) is ready
    Client3 (shared memory) is ready
    Server is ready. You can type intergers and then click [ENTER].
    Clients will show the mean, median, and mode of the input values:
    123 123 456 789
    Mean is 372.75
    Median is 289.5
    Mode is 123
    ```

<hr>

## Note

These warnings are bugs on `multiprocessing.shared_memory`:

```bash
/usr/lib/python3.8/multiprocessing/resource_tracker.py:216: UserWarning: resource_tracker: There appear to be 1 leaked shared_memory objects to clean up at shutdown
/usr/lib/python3.8/multiprocessing/resource_tracker.py:229: UserWarning: resource_tracker: '/MY_SHM': [Errno 2] No such file or directory: '/MY_SHM'
  warnings.warn('resource_tracker: %r: %s' % (name, e))
```

Reference: https://bugs.python.org/issue39959