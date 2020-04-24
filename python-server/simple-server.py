from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_GET(self, body=True):
        try:
            # req_header = self.parse_headers()
            self.send_response(200)
            self.send_resp_headers(req_header, 11)
            self.wfile.write('Hello world')
            return
        finally:
            self.finish()

if __name__ == '__main__':
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running')
    httpd.serve_forever()