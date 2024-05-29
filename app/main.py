import sys
import gzip
import socket
import socketserver
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Recieved {self.command} request for {self.path}")
        path_chunks = self.path.split("/")
        if path_chunks[1] == "":
            response = b"HTTP/1.1 200 OK\r\n\r\n"

        elif path_chunks[1] == "echo":
            response = self._get_echo_response(path_chunks)

        elif path_chunks[1] == "user-agent":
            response = self._get_user_agent_response()

        elif path_chunks[1] == "files":
            response = self._get_files_response(path_chunks)
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        self.wfile.write(response)

    def do_POST(self):
        print(f"Received {self.command} request for {self.path}")
        path_chunks = self.path.split("/")
        if path_chunks[1] == "":
            response = b"HTTP/1.1 200 OK\r\n\r\n"

        elif path_chunks[1] == "files":
            response = self._post_files_response(path_chunks)
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        self.wfile.write(response)


    def _get_echo_response(self, path_chunks) -> bytes:
        if len(path_chunks) < 3:
            return b"HTTP/1.1 400 Bad Request\r\n\r\n"

        response = "HTTP/1.1 200 OK\r\n"
        body = bytes(path_chunks[2], "utf-8")
        if self.headers.get("accept-encoding"):
            encoding = self.headers.get("accept-encoding", "")
            if "gzip" in encoding:
                response += "Content-Encoding: gzip\r\n"
                body = gzip.compress(body)

        response += "Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(body)}\r\n\r\n"
        response = bytes(response, 'utf-8')
        response += body

        return response

    def _get_user_agent_response(self) -> bytes:
        user_agent = self.headers.get("User-Agent")
        if not user_agent:
            return b"HTTP/1.1 400 Bad Request\r\n\r\n"

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(user_agent)}\r\n\r\n"
        response += user_agent
        response = bytes(response, 'utf-8')
        return response

    def _get_files_response(self, path_chunks) -> bytes:
        if len(path_chunks) < 3:
            return b"HTTP/1.1 400 Bad Request\r\n\r\n"

        filename = path_chunks[2]
        directory = sys.argv[2]

        try: 
            with open(directory+"/"+filename, 'r') as f:
                contents = f.read()
        except FileNotFoundError:
            return b"HTTP/1.1 404 Not Found\r\n\r\n"

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: application/octet-stream\r\n"
        response += f"Content-Length: {len(contents)}\r\n\r\n"
        response += contents
        response = bytes(response, 'utf-8')
        return response

    def _post_files_response(self, path_chunks) -> bytes:
        if len(path_chunks) < 3:
            return b"HTTP/1.1 400 Bad Request\r\n\r\n"

        filename = path_chunks[2]
        directory = sys.argv[2]
        filelength = int(self.headers['content-length'])
        filecontents = self.rfile.read(filelength)

        with open(directory+"/"+filename, 'w') as f:
            f.write(filecontents.decode('utf-8'))

        return b"HTTP/1.1 201 Created\r\n\r\n"



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
