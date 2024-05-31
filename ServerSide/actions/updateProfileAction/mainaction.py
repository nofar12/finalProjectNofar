import cgi
import os
from urllib.parse import parse_qs
from urllib.parse import urlparse
import datetime

import json
from ServerSide.database_manager import db_manager_instance
db_manager = db_manager_instance

class MainAction:
    def execute(self, HTTPReqHandler, username, userId):

        print("updateProfileAction self.path=" + HTTPReqHandler.path)
        content_length = int(HTTPReqHandler.headers['Content-Length'])


        form_data = cgi.FieldStorage(
            fp=HTTPReqHandler.rfile,
            headers=HTTPReqHandler.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        # parse the post data
        fileitem = form_data.getvalue('filename')
        filename = form_data.list[0].filename
        if fileitem:
            # strip the leading path from the file name
            fn = os.path.basename(username + "_" + filename)
            # open read and write the file into the server
            open("usersImages/" + fn, 'wb').write(fileitem)
            db_manager.execute_query("update users set profile_filename=? where id =?", ("/usersImages/" + fn,userId ) )

        HTTPReqHandler.send_response(302)  # redirect
        HTTPReqHandler.send_header('Location', '/accountSettings/accountSettings.html')  # Redirect to the profile page
        HTTPReqHandler.end_headers()
