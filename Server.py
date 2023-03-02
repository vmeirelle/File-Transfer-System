import socket
import threading
import os
import shutil

MAX_CACHE_SIZE = 1024*1024*64  # 64 MB

class FileTransferServer:
    def __init__(self, host, port, cache_folder, download_folder):
        self.host = host
        self.port = port
        self.cache_folder = cache_folder
        self.download_folder = download_folder
        self.cache = {}
        self.cache_size = 0
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def start(self):
        print(f"Server started on {self.host}:{self.port}")
        while True:
            client_socket, address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        print(f"Client connected: {client_socket.getpeername()}")
        while True:
            try:
                request = client_socket.recv(1024).decode().strip()
                if not request:
                    break
                command, *args = request.split()
                if command == "list":
                    response = "\n".join(os.listdir(self.cache_folder))
                    client_socket.send(response.encode())
                elif command == "get":
                    filename = args[0]
                    if filename in self.cache:
                        file_path = os.path.join(self.cache_folder, filename)
                        with open(file_path, "rb") as f:
                            data = f.read()
                        self.cache[filename] = self.cache.pop(filename)
                    else:
                        file_path = os.path.join(self.download_folder, filename)
                        with open(file_path, "rb") as f:
                            data = f.read()
                        if self.cache_size + len(data) > MAX_CACHE_SIZE:
                            self.evict()
                        with open(os.path.join(self.cache_folder, filename), "wb") as f:
                            f.write(data)
                        self.cache[filename] = data
                        self.cache_size += len(data)
                    client_socket.send(data)
            except Exception as e:
                print(f"Error while processing client request: {e}")
                break
        client_socket.close()
        print(f"Client disconnected: {client_socket.getpeername()}")

    def evict(self):
        if not self.cache:
            return
        filename, data = self.cache.popitem(last=False)
        self.cache_size -= len(data)
        os.remove(os.path.join(self.cache_folder, filename))

if __name__ == "__main__":
    server = FileTransferServer("localhost", 8080, "server_cache", "server_downloads")
    server.start()
