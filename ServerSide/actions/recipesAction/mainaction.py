from urllib.parse import parse_qs
from urllib.parse import urlparse
import json

from ServerSide.API_interaction import API_Interaction


class MainAction:
    def execute(self, HTTPReqHandler,username, userId):
        print("MainAction self.path=" + HTTPReqHandler.path)
        query_separate = parse_qs(urlparse(HTTPReqHandler.path).query)
        action = query_separate.get('action')[0]
        if action == 'random':
            data = API_Interaction.random_recipes()
            HTTPReqHandler.send_response(200)
            HTTPReqHandler.send_header('Content-type', 'application/json')
            HTTPReqHandler.end_headers()
            HTTPReqHandler.wfile.write(json.dumps(data).encode()) #convert a set of Python objects to a JSON string
            return
        if action == 'search':
            content_length = int(HTTPReqHandler.headers['Content-Length'])  # gets the size of data
            post_data = HTTPReqHandler.rfile.read(content_length)  # gets the data itself
            filterobj = json.loads(post_data)
            data = API_Interaction.search(filterobj)
            HTTPReqHandler.send_response(200)
            HTTPReqHandler.send_header('Content-type', 'application/json')
            HTTPReqHandler.end_headers()
            HTTPReqHandler.wfile.write(json.dumps(data).encode())
            return
