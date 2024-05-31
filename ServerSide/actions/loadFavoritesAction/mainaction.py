import json
import uuid
import cgi
import hashlib
from urllib.parse import unquote
from datetime import datetime, timedelta
from http import cookies

import bcrypt
from ServerSide.API_interaction import API_Interaction
from ServerSide.database_manager import db_manager_instance
db_manager = db_manager_instance

class MainAction:
    def execute(self, HTTPReqHandler, username, userId):
        favortiesRes = []
        likes_rcd_list = db_manager.execute_query_all("select recipeID, time from users_likes where userID=?", (userId,))
        if not likes_rcd_list or len(likes_rcd_list) == 0:
            HTTPReqHandler.send_response(200)
            HTTPReqHandler.send_header('Content-type', 'application/json')
            HTTPReqHandler.end_headers()
            HTTPReqHandler.wfile.write(json.dumps(favortiesRes).encode())
            return
        for fav_rcd in likes_rcd_list:
            recipe_data = API_Interaction.get_recipe_byID(fav_rcd[0])
            if recipe_data:
                recipeObj = recipe_data.get('recipe')
                favortiesRes.append(recipeObj)

        HTTPReqHandler.send_response(200)
        HTTPReqHandler.send_header('Content-type', 'application/json')
        HTTPReqHandler.end_headers()
        HTTPReqHandler.wfile.write(json.dumps(favortiesRes).encode())
