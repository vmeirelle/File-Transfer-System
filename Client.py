import socket

class FileTransferClient:
    def __init__(self, host, port):
        self.socket = socket.socket()
        self.socket.connect((host, port))

    def list_files(self):
        self.socket.send(b"list\n")
        data = self.socket.recv(1024)
        files = data.decode().split(",")
        print("Available files:")
        for filename in files:
            print(filename)

    def get_file(self, filename):
        self.socket.send(f"get {filename}\n".encode())
        data = self.socket.recv(1024*1024)  # 1 MB
        with open(f"client_files/{filename}", "wb") as f:
            f.write(data)
        print(f"{filename} downloaded")

if __name__ == "__main__":
    client = FileTransferClient("localhost", 8080)
    while True:
        command = input("Enter a command (list, get [filename], exit): ")
        if command == "list":
            client.list_files()
        elif command.startswith("get "):
            _, filename = command.split()
            client.get_file(filename)
        elif command == "exit":
            break
        else:
            print("Invalid command")
    client.socket.close()
