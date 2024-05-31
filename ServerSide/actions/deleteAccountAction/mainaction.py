from ServerSide.database_manager import db_manager_instance
db_manager = db_manager_instance
class MainAction:
    def execute(self, HTTPReqHandler,username, userId):
        #deleting user from users and log out
        # get the session ID
        session_id = HTTPReqHandler.get_cookieSession_id(HTTPReqHandler.headers)

        #delete the cookie
        if session_id:
            # db_manager.delete_session_byID(session_id)
            userID = db_manager.get_userID_bySessionID(session_id)
            if db_manager.delete_user_byID(userID): #true
                print("User was deleted")
                # redirect to homepage
                HTTPReqHandler.send_response(200)
                HTTPReqHandler.end_headers()
                return

        print("Failed - User was not deleted")
        HTTPReqHandler.send_response(400)
        HTTPReqHandler.end_headers()
        return
