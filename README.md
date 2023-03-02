# File Transfer System

This is a simple file transfer system consisting of a server and a client, implemented in Python. The system allows a client to request files from the server and download them to a local directory. The server caches recently requested files to improve performance.

## How it work's?

### Workflow

```css
            Client                                  Server
               |                                        |
               |    GET file_list()                     |
               |--------------------------------------->|
               |                                        |
               |    (List of files)                     |
               |<---------------------------------------|
               |                                        |
               |    GET file1.txt                       |
               |--------------------------------------->|
               |                                        |
               |    (file1.txt in cache?)               |
               |<---------------------------------------|
               |                                        |
     +---------+        (Yes)                           |
     | Cache? |  -------------------------------------->|
     +---------+                                        |
               |    Send file1.txt from cache           |
               |<---------------------------------------|
               |                                        |
               |    GET file2.txt                       |
               |--------------------------------------->|
               |                                        |
               |    (file2.txt in cache?)               |
               |<---------------------------------------|
               |                                        |
     +---------+        (No)                            |
     | Cache?  | -------------------------------------->|
     +---------+                                        |
               |    Fetch file2.txt from disk           |
               |<---------------------------------------|
               |                                        |
               |    Send file2.txt  to client           |
               |--------------------------------------->|
               |                                        |
       +------------------+                             |
       | Store file2.txt  |                             |
       | in cache         |                             |
       |----------------->|                             |
       |                  |                             |
       +------------------+                             |
```

1.  The client establishes a TCP connection with the server.
2.  The client sends a "list" command to the server, requesting a list of available files.
3.  The server responds with a list of filenames.
4.  The client sends a "get" command to the server, requesting a specific file.
5. If the requested file is in the server cache, the server sends the file contents from memory.
6. If the requested file is not in the cache, the server reads the file from disk and sends it to the client. The server also adds the file to the cache.
7. The client receives the file contents and saves it to a local directory.
8. Steps 4-7 can be repeated multiple times for different files.
9.  When the client is finished, it sends a "quit" command to the server to close the TCP connection.

## Architecture
The system follows a client-server architecture, where the client sends requests to the server, and the server responds with the requested files. The communication between the client and the server is done over a TCP connection. The system uses multi-threading to handle multiple client connections concurrently.

## Technologies
The system is implemented in Python 3. The following Python modules are used:

```socket```: for establishing a TCP connection between the client and the server.

```threading```: for handling multiple client connections concurrently.

```os``` and ```shutil```: for managing files and directories.

```time```: for calculating the age of cached files.

## Protocols

The system uses a custom text-based protocol to communicate between the client and the server. The protocol consists of two commands:

```list```: sends a list of filenames that are available on the server.

```get <filename>```: sends the contents of the specified file to the client.

## Design Decisions

### Server Cache
To improve performance, the server caches recently requested files in memory. The cache has a maximum size, and if the cache exceeds that size, the cache won't get more files. The cache is implemented as a Python dictionary, where the keys are the filenames, and the values are the file contents.

### File Structure
The server stores the files that can be requested by clients in a directory called server_downloads. The files that are cached are stored in a separate directory called server_cache.

### Multi-Threading
The system uses multi-threading to handle multiple client connections concurrently. When a new client connects to the server, a new thread is created to handle the client's requests.

## Solutions to Critical Problems
### File Caching
One critical problem that the system solves is the time it takes to send large files over a network. To address this problem, the system implements a file caching mechanism on the server. When a client requests a file, the server first checks if the file is in the cache. If the file is in the cache, the server sends the file contents from memory. If the file is not in the cache, the server reads the file from disk and sends it to the client. The server also adds the file to the cache, so that subsequent requests for the same file can be served more quickly.

### Cache Size Limit
Another critical problem that the system solves is the size of the file cache. To ensure that the cache does not consume too much memory, the server limits the size of the cache. 
  
## Conclusion
In conclusion, the file transfer system is a simple but effective solution for transferring files between a server and multiple clients. The system's architecture is based on a client-server model, and the communication between the client and the server is done using a custom text-based protocol over a TCP connection. The system's design decisions, such as file caching and multi-threading, address critical problems such as slow file transfers and limited memory resources. Overall, the system is a practical solution for transferring files over a network in a secure and efficient manner.
