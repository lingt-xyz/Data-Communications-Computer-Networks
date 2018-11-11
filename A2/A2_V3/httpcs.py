from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'This is a get request')


    def do_POST(self):
        content_length = int(self.headers['Content-length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO
        response.write(b'This is a post request')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

httpd = HTTPServer(('localhost', 8090), SimpleHTTPRequestHandler)
httpd.serve_forever()