import cgi
import uuid
import cgi
from urllib.parse import unquote

import bcrypt

from ServerSide.database_manager import db_manager_instance
db_manager = db_manager_instance

class MainAction:
    def execute(self, HTTPReqHandler, username, userId):

        print("changePasswordAction self.path=" + HTTPReqHandler.path)
        content_length = int(HTTPReqHandler.headers['Content-Length'])


        form_data = cgi.FieldStorage(
            fp=HTTPReqHandler.rfile,
            headers=HTTPReqHandler.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        # parse the post data
        new_password = unquote(form_data.getvalue('password')) # unquote() - decodes special characters
        confirm_password = unquote(form_data.getvalue('confirm-password'))
        message = None
        if len(new_password)>20 or len(confirm_password)>20:
            message = "Please enter up to 20 characters."

        if new_password != confirm_password:
            message = "Passwords aren't matching. Try again."

        if message:
            HTTPReqHandler.send_response(409)  # Conflict status code
            HTTPReqHandler.send_header('Content-type', 'text/plain')
            HTTPReqHandler.end_headers()
            HTTPReqHandler.wfile.write(message)
            return

        #convert to bytes
        password_bytes = new_password.encode('utf-8')
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        hashPassword = bcrypt.hashpw(password_bytes, salt)
        db_manager_instance.execute_query("update users set password=?, salt=? where id=?", (hashPassword, salt, userId))

        HTTPReqHandler.send_response(200)  #OK
        HTTPReqHandler.send_header('Content-type', 'text/plain')
        HTTPReqHandler.end_headers()
        HTTPReqHandler.wfile.write(b"Password was changed successfully!")
        return

