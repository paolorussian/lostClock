#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_rensponse(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Hello world!"
        self.wfile.write(bytes(message, "utf8"))
        return

    def run():
        print('Avvio del server...')
        server_address = ('127.0.0.1', 8081)
        httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        print('Server in esecuzione...')
        httpd.serve_forever()

    run()
