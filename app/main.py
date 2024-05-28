import socket


def main():
    print("Logs from your program will appear here!")

    server_socket: socket.socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept()# wait for client

def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")
    client_socket.recv(1024)
    response = "HTTP/1.1 200 OK\r\n\r\n"
    client_socket.send(response.encode())
    client_socket.close()


def start_server(host, port):
    server = socket.create_server((host, port), reuse_port=True)
    server.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, address = server.accept()
        handle_client(client_socket, address)




if __name__ == "__main__":
    host = "localhost"
    port = 4221
    start_server(host, port)
