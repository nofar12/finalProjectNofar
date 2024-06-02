from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import re
import ssl
from ServerSide.controllers.BaseController import BaseHttpController
from ServerSide.database_manager import db_manager_instance
from ServerSide.globals import LISTEN_PORT, LISTEN_HOST

db_manager = db_manager_instance


class HTTPReqHandler(BaseHTTPRequestHandler):  # Requests Handler
    root_dir = os.path.dirname(os.path.abspath(__file__))

    def handle(self):  # Override
        print(f"Client connected: {self.client_address} ")
        super().handle()  # Call the parent's class method

    def do_GET(self):
        try:
            BaseHttpController.handle(self)
        except Exception as e:
            print("Got exception!!")
            print(e)
            self.send_header('Content-type', 'text/html')
            self.send_response(302)
            self.send_header('Location', "notFound/pageNotFound.html")  # Redirect to the error page
            self.end_headers()
            return


    def do_POST(self):
        try:
            BaseHttpController.handle(self)
        except Exception as e:
            print(e)
            self.send_response(404)  # not found
            self.end_headers()

    def is_email_valid(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))  # boolean

    def is_username_valid(self, username):
            return bool(username.isalnum())  # boolean

    def get_cookieSession_id(self, headers):
        try:
            if headers.get('Cookie'):
                cookie = headers.get('Cookie').split(';')  # split the value of "Cookie" header from the client's request
                for x in cookie:
                    name, value = x.strip().split("=")
                    if name == "session_id":
                        print("session id found!")
                        return value
            print("no session id found")
            return None
        except Exception as e:
            print(e)
            return None


def run_server():
    server_address = ('', LISTEN_PORT)
    httpd = HTTPServer(server_address, HTTPReqHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)
    print('Starting server... listen on ' + LISTEN_HOST + ":" + str(LISTEN_PORT))
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
