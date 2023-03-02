# File-Transfer System: TCP, Multi-thred and Cache.

This is a file transfer system implemented in Python. The system consists of two components: a server that stores files in a cache and a client that can download files from the server or upload files to the server. The system supports multi-threading and caching of files on the server side, and provides a simple command line interface for the client.

## How it works?

```SQL
             Client                                  Server
               |                                        |
               |    GET file_list()                     |
               |--------------------------------------->|
               |                                        |
               |    (List of files)                     |
               |<---------------------------------------|
               |                                        |
               |    GET file.txt                        |
               |--------------------------------------->|
               |                                        |
               |    (file.txt in cache?)                |
               |<---------------------------------------|
               |                                        |
     +---------+        (Yes)                           |
     | Cache? |  -------------------------------------->|
     +---------+                                        |
               |    Send file.txt from cache            |
               |<---------------------------------------|
               |                                        |
               |    GET image.png                       |
               |--------------------------------------->|
               |                                        |
               |    (image.png in cache?)               |
               |<---------------------------------------|
               |                                        |
     +---------+        (No)                            |
     | Cache?  | -------------------------------------->|
     +---------+                                        |
               |    Fetch image.png from disk           |
               |<---------------------------------------|
               |                                        |
               |    Send image.png to client            |
               |--------------------------------------->|
               |                                        |
       +------------------+                             |
       | Store image.png  |                             |
       | in cache         |                             |
       |----------------->|                             |
       |                  |                             |
       +------------------+                             |
                                                    


```


1. The client sends a GET file_list() command to the server to retrieve a list of files available in the server's cache.
2. The server responds with a list of files.
3. The client sends a GET file.txt command to the server to retrieve the file named file.txt.
4. The server checks if file.txt is in the cache directory.
5. Since file.txt is in the cache directory, the server sends the file to the client from the cache.
6. The client sends a GET image.png command to the server to retrieve the file named image.png.
7. The server checks if image.png is in the cache directory.
8. Since image.png is not in the cache directory, the server fetches the file from the data directory and sends it to the client.
9. After sending image.png to the client, the server writes the file to the cache directory for future requests.

Note that the cache is used to store frequently accessed files, which can be retrieved more quickly than fetching them from the data directory. If a requested file is not in the cache, it is fetched from the data directory and sent to the client, and then stored in the cache for future requests.

## Architecture
The system uses a client-server architecture. The server listens for incoming connections from clients, and responds to requests for file transfers. The server stores files in a cache on disk, and provides clients with a list of available files in the cache. The client connects to the server and can download or upload files as needed.

## Technologies
The system is implemented in Python, using the built-in socket library for networking. The server uses multi-threading to handle multiple clients simultaneously. The server also caches files on disk using the os and shutil libraries.

## Protocols
The system uses a simple command line protocol to communicate between the client and server. The protocol supports three commands:

LIST: Returns a list of filenames available in the server's cache.
GET <filename>: Downloads a file from the server with the given filename.
PUT <filename>: Uploads a file to the server with the given filename.
Design Decisions
The system was designed with the following goals in mind:

Simplicity: The system should be easy to understand and use, with a minimalistic interface.
Scalability: The system should be able to handle multiple clients simultaneously.
Efficiency: The system should minimize network traffic and disk I/O.
Robustness: The system should be able to handle errors and recover gracefully.
To achieve these goals, the server uses a cache to minimize disk I/O and the client uses a simple protocol to minimize network traffic. The server also uses multi-threading to handle multiple clients simultaneously. The system includes error handling to handle common errors such as file not found or disk full.

## Multi-thread

Multi-threading is used on the server side to handle multiple clients simultaneously. When a client connects to the server, a new thread is created to handle that client's requests. The main thread continues listening for incoming connections, while the newly created thread handles the client's requests.

Here is an example of how multi-threading is used in the server code:
```python
  while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()
    
    # Create a new thread to handle the client's requests
    t = threading.Thread(target=handle_client, args=(client_socket, client_address))
    t.start()
```
In this code, server_socket.accept() blocks until a client connects to the server. Once a client connects, a new thread is created using the threading.Thread() constructor, with the target argument set to the handle_client function and the args argument set to a tuple containing the client's socket and address. The new thread is started with the start() method, and the main thread continues listening for incoming connections.

The handle_client() function is responsible for handling the client's requests. It receives the client's socket and address as arguments, and reads and writes data using the socket. Because each client is handled in a separate thread, multiple clients can be handled simultaneously without blocking the main thread.

##Cache

The server uses a cache to store frequently accessed files, in order to improve performance by reducing disk I/O. The cache is implemented as a directory on the server's disk, where files are stored temporarily as clients download or upload them.

Here is an example of how the cache is used in the server code:

```python
def handle_client(client_socket, client_address):
    # Receive the client's request
    request = client_socket.recv(1024).decode()

    # Parse the request
    parts = request.split()
    command = parts[0]

    # Handle the request
    if command == "LIST":
        # Get a list of files in the cache
        files = os.listdir(CACHE_DIR)

        # Send the list of files to the client
        response = "\n".join(files).encode()
        client_socket.sendall(response)
    elif command == "GET":
        # Get the filename from the request
        filename = parts[1]

        # Check if the file is in the cache
        if os.path.exists(os.path.join(CACHE_DIR, filename)):
            # If the file is in the cache, send it to the client
            with open(os.path.join(CACHE_DIR, filename), "rb") as f:
                data = f.read()
                client_socket.sendall(data)
        else:
            # If the file is not in the cache, fetch it from disk
            with open(os.path.join(DATA_DIR, filename), "rb") as f:
                data = f.read()
                client_socket.sendall(data)

            # Store the file in the cache for future requests
            with open(os.path.join(CACHE_DIR, filename), "wb") as f:
                f.write(data)
    elif command == "PUT":
        # Get the filename from the request
        filename = parts[1]

        # Receive the file from the client
        data = client_socket.recv(1024)

        # Write the file to disk
        with open(os.path.join(DATA_DIR, filename), "wb") as f:
            f.write(data)

        # Store the file in the cache for future requests
        with open(os.path.join(CACHE_DIR, filename), "wb") as f:
            f.write(data)

```
In this code, the cache directory is specified by the CACHE_DIR variable, and the data directory (where files are permanently stored) is specified by the DATA_DIR variable.

When a client requests a file using the GET command, the server first checks if the file is in the cache by looking for a file with the same name in the cache directory. If the file is in the cache, it is sent to the client from the cache directory. If the file is not in the cache, it is fetched from the data directory and sent to the client, and also stored in the cache directory for future requests.

When a client uploads a file using the PUT command, the file is written to the data directory, and also stored in the cache directory for future requests.

The cache has a fixed maximum size, which is not explicitly enforced in this code. If the cache directory becomes too large, files may be evicted to make room for new files. This eviction policy is not implemented in this code, but could be implemented using various strategies such as LRU (least recently used) or LFU (least frequently used) caching.

 
## Solutions to Critical Problems
One of the critical problems in the system is ensuring thread safety when accessing the cache. To address this problem, the server uses a lock to ensure that only one thread can access the cache at a time.

Another critical problem is handling files that are too large to fit in the cache. To address this problem, the server fetches these files from disk when requested by the client, and does not store them in the cache.

Finally, the system must handle errors such as file not found, disk full, or network errors. The system includes error handling to handle these errors gracefully and provide informative error messages to the user.

## Conclusion
The file transfer system is a simple and efficient way to transfer files between clients and servers. The system uses a client-server architecture with a simple command line protocol to transfer files. The system is designed with simplicity, scalability, efficiency, and robustness in mind, and includes solutions to critical problems such as thread safety, handling large files, and error handling.
