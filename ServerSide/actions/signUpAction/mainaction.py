import bcrypt as bcrypt
import uuid
import cgi
from urllib.parse import unquote
from datetime import datetime, timedelta
from http import cookies
from ServerSide.database_manager import db_manager_instance

db_manager = db_manager_instance

class MainAction:

    def execute(self, HTTPReqHandler,username, userId):
        print("signUpAction self.path=" + HTTPReqHandler.path)
        content_length = int(HTTPReqHandler.headers['Content-Length'])
        # read the post data
        form_data = cgi.FieldStorage(
            fp=HTTPReqHandler.rfile,
            headers=HTTPReqHandler.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        username = unquote(form_data.getvalue('username'))  # unquote() - decodes special characters
        email = unquote(form_data.getvalue('email'))
        password = unquote(form_data.getvalue('password'))

        # create users and sessions table if not exists
        #db_manager.create_table("users","id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL, img_filename varchar(255) DEFAULT 'profilePicture.png', salt TEXT")
        #db_manager.create_table("sessions","session_id TEXT PRIMARY KEY, user_id INTEGER,  creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  expiration_timestamp TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id)")  # create sessions table if not exists

        message = ""

        # check lengths
        if len(username)>20 or len(email)>20 or len(str(password))>20:
            message = b'Please enter up to 20 characters.'
        # check if username is valid
        if not HTTPReqHandler.is_username_valid(username) :
                message = b'Username is not valid. Try again.'

        # check if email is valid
        if not HTTPReqHandler.is_email_valid(email):
            message = b'Email is not valid. Try again.'

        # check if username or email already exists in the database
        if db_manager.check_username_exists(username) and db_manager.check_email_exists(email):
            message = b'Username and Email are taken. Try again.'
        elif db_manager.check_username_exists(username):
            message = b'Username is taken. Try again.'
        elif db_manager.check_email_exists(email):
            message = b'Email is taken. Try again.'

        confirm_password =unquote(form_data.getvalue('confirm-password'))

        if password != confirm_password:
            message = b"Passwords aren't matching. Try again."

        if message:
            HTTPReqHandler.send_response(409)  # Conflict status code
            HTTPReqHandler.send_header('Content-type', 'text/plain')
            HTTPReqHandler.end_headers()
            HTTPReqHandler.wfile.write(message)
            return

        #convert to bytes
        password_bytes = password.encode('utf-8')
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        hashPassword = bcrypt.hashpw(password_bytes, salt)

        values = (username, email, hashPassword, salt)
        query = "INSERT INTO users (username, email, password, salt ) VALUES (?,?,?,?)"  # the ? is parameters placeholders
        db_manager.execute_query(query, values)

        query = "INSERT INTO sessions (session_id, user_id, expiration_timestamp) VALUES (?,?,?)"  # the ? is parameters placeholder
        session_id = str(uuid.uuid4()) #create unique session ID
        expiration_time = datetime.now() + timedelta(hours=24)  # expiration_time in a day
        values = (session_id, db_manager.get_user_id_byUsername(username), expiration_time)
        db_manager.execute_query(query, values)

        cookie = cookies.SimpleCookie()
        cookie['session_id'] = session_id
        cookie['session_id']['expires'] = expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')  # browser format
        cookie['session_id']['path'] = '/'  # means that the cookie is valid for the entire domain/website

        HTTPReqHandler.send_response(302)  #  redirect
        HTTPReqHandler.send_header('Location', '/userRecipeSearch/discoverRecipes.html')  # Redirect to the profile page
        HTTPReqHandler.send_header('Set-Cookie',cookie['session_id'].OutputString())  # Include the cookie in the response
        HTTPReqHandler.end_headers()

