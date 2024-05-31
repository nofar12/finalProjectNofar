import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from importlib import import_module
from ServerSide.database_manager import db_manager_instance

#from database_manager import db_manager_instance
from ServerSide.globals import LISTEN_PORT, LISTEN_HOST

db_manager = db_manager_instance
class BaseHttpController:

    fileTypeDic = { # the file types the client can have access to
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "png": "image/png",
        "woff": "application/font-woff",
        "woff2": "application/font-woff2"
    }

    actionMappingDic = {
        "submit_form_signUp": "ServerSide.actions.signUpAction.mainaction",
        "submit_form_logIn": "ServerSide.actions.loginAction.mainaction",
        "recipesAction": "ServerSide.actions.recipesAction.mainaction",
        "view_recipe": "ServerSide.actions.viewRecipeAction.mainaction",
        "sumbit_review": "ServerSide.actions.sumbitReviewAction.mainaction",
        "log_out": "ServerSide.actions.logOutAction.mainaction",
        "delete_account": "ServerSide.actions.deleteAccountAction.mainaction",
        "update_profile": "ServerSide.actions.updateProfileAction.mainaction",
        "change_password": "ServerSide.actions.changePasswordAction.mainaction",
        "load_favorites" :"ServerSide.actions.loadFavoritesAction.mainaction",
    }


    @staticmethod
    def handle(HTTPReqHandler):
        requestPath = urlparse(HTTPReqHandler.path)
        path = HTTPReqHandler.path.lstrip('/')  # removing leading slash from the requested path
        file_path = os.path.join(HTTPReqHandler.root_dir, path.lstrip('/'))  # Join the root dir to the path

        # checking if the request is for file content (html,css, js..)
        if BaseHttpController.handleFilerequest(HTTPReqHandler, file_path) == True:
            print("BaseHttpController: It was file request")
            return

        action = requestPath.path[HTTPReqHandler.path.rfind("/") + 1:]
        print("BaseHttpController: Try to handle action=" + action)

        # match the action name based on the dictionary
        action_class_module_str = BaseHttpController.actionMappingDic.get(action)
        #get user's session id
        session_id = HTTPReqHandler.get_cookieSession_id(HTTPReqHandler.headers)
        #get username
        username = db_manager.get_username_bySessionID(session_id)
        if action_class_module_str is None or \
                        action_class_module_str != "ServerSide.actions.signUpAction.mainaction" and \
                        action_class_module_str != "ServerSide.actions.loginAction.mainaction" and \
                       not username : #no valid action or not logged in
            HTTPReqHandler.send_response(302)
            HTTPReqHandler.send_header('Location', "/homepage/homepage.html")
            HTTPReqHandler.end_headers()
            return
        print("Import module=" + action_class_module_str)  # print the module name that will be imported
        imp = import_module(action_class_module_str) # import the module dynamically
        actionClass = getattr(imp, "MainAction") # get the "MainAction" class from the imported module
        actionObj = actionClass() # create instance of the MainAction class
        userID = db_manager.get_userID_bySessionID(session_id) # get the user's ID from the database by their session ID
        actionObj.execute(HTTPReqHandler,username, userID) # execute the "execute" method of the MainAction instance




    @staticmethod
    def handleFilerequest(HTTPReqHandler, file_path):
        if HTTPReqHandler.path.rfind(".") == -1: # checks if the requested path doesn't contains a dot (file extension like, .html)
            return False

        fileType = HTTPReqHandler.path[HTTPReqHandler.path.rfind(".")+1:] # extracts the file extension
        contentType = BaseHttpController.fileTypeDic.get(fileType) # match the content type based on the dictionary
        if contentType: # Not None (means it's a request for an allowed access file)
            print("BaseHttpController: fileType=" + fileType)
            if not os.path.exists(file_path):  # Check if the file isn't exists
                print("File not found =" + file_path)
                HTTPReqHandler.send_response(302)
                HTTPReqHandler.send_header('Location', "/notFound/pageNotFound.html")
                HTTPReqHandler.end_headers()
                return True

            session_id = None

            if fileType == "html":
                db_manager.delete_expired_sessions()
                session_id = HTTPReqHandler.get_cookieSession_id(HTTPReqHandler.headers)

                if session_id: #user is logged in
                    print("BaseHttpController: found sessionId=" + session_id)
                    user_rcd = db_manager.get_user_detail_from_session(session_id)
                    if user_rcd:
                        print("Username found:", user_rcd.get("username"))
                        if "homepage.html" in file_path:  # logged-in user trying to access the non-logged-in homepage
                           HTTPReqHandler.send_response(302)
                           HTTPReqHandler.send_header('Location', "/homepageUser/homepageUser.html")
                           HTTPReqHandler.end_headers()
                           return True
                        with open(file_path, 'rb') as file:
                           HTTPReqHandler.send_response(200)
                           HTTPReqHandler.send_header('Content-type', contentType)
                           updated_content = file.read().replace(b'Loading...', user_rcd.get("username").encode())
                           updated_content = updated_content.replace(b'profilePicture...', user_rcd.get("profile_filename").encode())

                           HTTPReqHandler.send_header('Content-Length', str(len(updated_content)))
                           HTTPReqHandler.end_headers()
                           HTTPReqHandler.wfile.write(updated_content)
                           return True
                if "homepage.html" not in file_path and \
                        "logIn.html" not in file_path and \
                        "signUp.html" not in file_path:
                    HTTPReqHandler.send_response(302)# session expired - non-logged-in user trying to access the logged-in  homepage
                    HTTPReqHandler.send_header('Location', "/homepage/homepage.html")
                    HTTPReqHandler.end_headers()
                    return True

            with open(file_path, 'rb') as file:
                HTTPReqHandler.send_response(200)
                HTTPReqHandler.send_header('Content-type', contentType)
                HTTPReqHandler.send_header('Content-Length', str(os.path.getsize(file_path)))
                HTTPReqHandler.end_headers()
                HTTPReqHandler.wfile.write(file.read())
        return True
