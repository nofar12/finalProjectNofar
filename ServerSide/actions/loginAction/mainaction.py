import uuid
import cgi
import hashlib
from urllib.parse import unquote
from datetime import datetime, timedelta
from http import cookies

import bcrypt

from ServerSide.database_manager import db_manager_instance
db_manager = db_manager_instance

class MainAction:
    def execute(self, HTTPReqHandler, username, userId):
        content_length = int(HTTPReqHandler.headers['Content-Length'])

        # read the post data
        form_data = cgi.FieldStorage(
            fp=HTTPReqHandler.rfile,
            headers=HTTPReqHandler.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        usernameOrEmail = unquote(form_data.getvalue('usernameOrEmail'))  # unquote() function decodes special characters.
        email = ''
        username = ''


        # check length
        if len(usernameOrEmail)>20 or len(form_data.getvalue('password')) > 20:
            HTTPReqHandler.send_response(409)  # Conflict status code
            HTTPReqHandler.send_header('Content-type', 'text/plain')
            HTTPReqHandler.end_headers()
            HTTPReqHandler.wfile.write(b'Please enter up to 20 characters.')
            return

        if HTTPReqHandler.is_email_valid(usernameOrEmail):  # check if match to email pattern
            email = usernameOrEmail
        else:
            username = usernameOrEmail

        values = (username, email)
        query = "SELECT * FROM users WHERE username=? OR email=?"  # return all the records with the info
        user_data = db_manager.execute_query(query, values)  # the user's specific data record based on username/email
        message = ""

        if user_data:
            stored_password = user_data[3]
            stored_salt = user_data[5]
            input_password = unquote(form_data.getvalue('password')).encode('utf-8') #convert to bytes
            formpass = bcrypt.hashpw(input_password, stored_salt) # hashing the inputed password with the stoeed salt
            if stored_password == formpass:  # correct password

                query = "INSERT INTO sessions (session_id, user_id, expiration_timestamp) VALUES (?,?,?)"  # the ? is parameters placeholder
                session_id = str(uuid.uuid4())
                expiration_time = datetime.now() + timedelta(hours=24)  # expiration_time in a day
                values = (session_id, db_manager.get_user_id_byUsername(username), expiration_time)
                db_manager.execute_query(query, values)

                cookie = cookies.SimpleCookie()
                cookie['session_id'] = session_id
                cookie['session_id']['expires'] = expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')  # browser format
                cookie['session_id']['path'] = '/'  # means that the cookie is valid for the entire domain/website

                HTTPReqHandler.send_response(302)  #  redirect
                HTTPReqHandler.send_header('Location','/userRecipeSearch/discoverRecipes.html')  # Redirect to the discovery page
                HTTPReqHandler.send_header('Set-Cookie',cookie['session_id'].OutputString())  # Include the cookie in the response
                HTTPReqHandler.end_headers()
                return
            else:  # incorrect password
                message = b"Incorrect password. Try again."

        else:  # user_data is none (Null)
            message = b"User does not exist."

        HTTPReqHandler.send_response(409)  # Conflict status code
        HTTPReqHandler.send_header('Content-type', 'text/plain')
        HTTPReqHandler.end_headers()
        HTTPReqHandler.wfile.write(message)
