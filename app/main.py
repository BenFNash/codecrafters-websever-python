import socketserver
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Recieved GET request for {self.path}")
        path_chunks = self.path.split("/")
        if path_chunks[1] == "":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path_chunks[1] == "echo":
            response = "HTTP/1.1 200 OK\r\n\r\n"
            response += "Content-Type: text/plain\r\n"
            response += f"Content-Length: {len(path_chunks[1])}\r\n\r\n"
            response += path_chunks[2]
            print(response)
            response = bytes(response, 'utf-8')

        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        self.wfile.write(response)

    def do_POST(self):
        ...



# def handle_client(client_socket, address):
#     print(f"Accepted connection from {address}")
#     request = client_socket.recv(1024).decode("utf-8")
#
#     path = request.split(" ")[1]
#     if path == "/":
#         response = "HTTP/1.1 200 OK\r\n\r\n"
#     else:
#         response = "HTTP/1.1 404 Not Found\r\n\r\n"
#     
#     client_socket.send(response.encode())
#     client_socket.close()


# def start_server(host, port):
#     server = socket.create_server((host, port), reuse_port=True)
#     server.listen(1)
#     print(f"Server listening on {host}:{port}")
#
#     while True:
#         client_socket, address = server.accept()
#         handle_client(client_socket, address)

def start_server(host, port):
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        print(f"Server listening on {host}:{port}")
        server.serve_forever()




if __name__ == "__main__":
    host = "localhost"
    port = 4221
    start_server(host, port)
