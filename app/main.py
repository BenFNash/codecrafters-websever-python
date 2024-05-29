import socket
import socketserver
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Recieved GET request for {self.path}")
        path_chunks = self.path.split("/")
        if path_chunks[1] == "":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path_chunks[1] == "echo":
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/plain\r\n"
            response += f"Content-Length: {len(path_chunks[2])}\r\n\r\n"
            response += path_chunks[2]
            response = bytes(response, 'utf-8')
        elif path_chunks[1] == "user-agent":
            user_agent = self.headers.get("User-Agent")
            if user_agent:
                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type: text/plain\r\n"
                response += f"Content-Length: {len(user_agent)}\r\n\r\n"
                response += user_agent
                response = bytes(response, 'utf-8')
            else:
                response = b"HTTP/1.1 400 Bad Request\r\n\r\n"


        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        self.wfile.write(response)

    def do_POST(self):
        ...


def start_server(host, port):
    with socketserver.TCPServer((host, port), RequestHandler, bind_and_activate=False) as server:
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server.server_bind()
        server.server_activate()
        print(f"Server listening on {host}:{port}")
        server.serve_forever()




if __name__ == "__main__":
    host = "localhost"
    port = 4221
    start_server(host, port)
