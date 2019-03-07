import time
import templey
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 9000


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.respond({'status': 200})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        if path.endswith(".css"):
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                content = open("site" + path,"r").read()
                return bytes(content, 'UTF-8')
        else:
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                if path == "/":
                    path = "/index.html"
                content = templey.processFile("site" + path,"")
                return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

server_class = HTTPServer
httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
   pass
httpd.server_close()
print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
