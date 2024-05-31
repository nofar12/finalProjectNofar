from ServerSide.database_manager import db_manager_instance
db_manager = db_manager_instance
class MainAction:
    def execute(self, HTTPReqHandler,username, userId):
        #deleting session of the user
        # get the session ID
        session_id = HTTPReqHandler.get_cookieSession_id(HTTPReqHandler.headers)

        #delete the session
        if session_id:
            db_manager.delete_session_byID(session_id)
            print("logged out")
            HTTPReqHandler.send_response(200)
            HTTPReqHandler.end_headers()
            return
        else:
            print("Logout failed")
            HTTPReqHandler.send_response(400)
            HTTPReqHandler.end_headers()
            return
