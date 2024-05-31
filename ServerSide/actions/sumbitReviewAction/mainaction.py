from urllib.parse import parse_qs
from urllib.parse import urlparse
import datetime

import json
from ServerSide.database_manager import db_manager_instance
db_manager = db_manager_instance

class MainAction:
    def execute(self, HTTPReqHandler, username, userId):
        print("sumbitReviewAction self.path=" + HTTPReqHandler.path)
        content_length = int(HTTPReqHandler.headers['Content-Length'])

        # parse the post data
        post_data = HTTPReqHandler.rfile.read(content_length)
        reviewObj = json.loads(post_data)
        print(reviewObj)
        # extract data from the request
        user_input = reviewObj.get("user_input")
        recipe_id = reviewObj.get("recipe_id")


        #find the userID who sent the review
        session_id = HTTPReqHandler.get_cookieSession_id(HTTPReqHandler.headers)
        if session_id is not None:
             print("BaseHttpController: found sessionId=" + session_id)
             user_rcd = db_manager.get_user_detail_from_session(session_id)

             print("UserID found:", user_rcd.get("id"))
             #add the review to the reviews database
             params = (recipe_id,user_input,user_rcd.get("id"))
             query = "INSERT INTO reviews (recipeID, reviewContent,userID) VALUES (?,?,?)"  # the ? is parameters placeholders
             db_manager.execute_query(query, params)
             data ={"username":user_rcd.get("username"), "review":user_input,"time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "profile_pic":user_rcd.get("profile_filename") }
             HTTPReqHandler.send_response(200)
             HTTPReqHandler.send_header('Content-type', 'application/json')
             HTTPReqHandler.end_headers()
             HTTPReqHandler.wfile.write(json.dumps(data).encode())
        else:
            print("no session id")
