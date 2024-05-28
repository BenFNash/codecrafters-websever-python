import socket

def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")
    request = client_socket.recv(1024).decode("utf-8")

    path = request.split(" ")[1]
    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    
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
