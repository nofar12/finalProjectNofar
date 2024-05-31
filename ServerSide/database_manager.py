import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection()

        #self.conn = None

    def connection(self):  # connect the server to the user database
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Connected to the {self.db_name} database")
        except sqlite3.Error as e:
            print("Error connecting to users database:", e)
        return self.conn

    def create_table(self, table_name, structure):
        try:
            cursor = self.conn.cursor()# for executing SQL queries
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({structure})")  # automatically committed to the database when executed
            self.conn.commit()

        except sqlite3.Error as e:
            print("Error creating table:" + str(e))

    def execute_query(self, query, params=None):
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            print("Query executed successfully")
            return cursor.fetchone()  # Return fetched data
        except sqlite3.Error as e:
            print("Error executing query:", e)

    def execute_query_all(self, query, params=None):
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            print("Query executed successfully")
            return cursor.fetchall()  #Fetches all rows
        except sqlite3.Error as e:
            print("Error executing query:", e)

    def check_username_exists(self, username):
        # Check if the username already exists in the database
        try:
            #cursor = self.conn.cursor()
            #cursor.execute("SELECT username FROM users WHERE username=?", (username,))
            return self.execute_query("SELECT id FROM users WHERE username=?", (username,)) is not None #boolean
        except sqlite3.Error as e:
            print("Error checking username:", e)
            return False


    def check_email_exists(self, email):
            # Check if the email already exists in the database
            try:
                #cursor = self.conn.cursor()
                #cursor.execute("SELECT email FROM users WHERE email=?", (email,))
                return  self.execute_query("SELECT email FROM users WHERE email=?", (email,)) is not None #boolean
            except sqlite3.Error as e:
                print("Error checking email:", e)
                return False

    def get_user_id_byUsername(self, username):
            # Get userID by username
            try:
                result = self.execute_query("SELECT id FROM users WHERE username=?", (username,))
                if result:
                    return result[0]  # Return the user ID if found
                return None
            except sqlite3.Error as e:
                print("Error getting user ID:", e)
                return None

    def get_username_bySessionID(self,session_id):
        # Get username by session_id
        try:
            resultTup = self.execute_query("SELECT user_id FROM sessions WHERE session_id=?", (session_id,)) #tuple
            if not resultTup:
                return None

            user_id = resultTup[0]
            return self.execute_query("SELECT username FROM users WHERE id=?", (user_id,))[0]
        except sqlite3.Error as e:
            print("Error getting username:", e)
            return None
        except sqlite3.Error as e:
            print("Error is_recipePageID_exist :", e)
            return False

    def get_userID_bySessionID(self, session_id):
        # Get userID by session_id
        try:
            # result = self.execute_query("SELECT user_id FROM sessions WHERE session_id=?", (session_id,))
            # if not result:
            #     return None
            # return result[0]
            username = self.get_username_bySessionID(session_id)
            return self.get_user_id_byUsername(username)
        except sqlite3.Error as e:
            print("Error getting userID:", e)
            raise Exception("Error getting userID")


    def get_user_detail(self, user_id):
        user_rcd = self.execute_query("SELECT id,username,email,profile_filename,password,salt FROM users WHERE id=?", (user_id,))
        if not user_rcd:
            return None

        userDic = {
            "id": user_rcd[0],
            "username": user_rcd[1],
            "email": user_rcd[2],
            "profile_filename": user_rcd[3],
            "password": user_rcd[4],
            "salt": user_rcd[5]
        }

        return userDic

    def get_user_detail_from_session(self, session_id):
        #session_rcd = self.execute_query("SELECT user_id FROM sessions WHERE session_id=?", (session_id,))
        # Get the record of the
        session_rcd = self.get_userID_bySessionID(session_id)
        if not session_rcd:
            return  None
        #return self.get_user_detail(session_rcd[0])
        return self.get_user_detail(session_rcd)


    def delete_expired_sessions(self):
        try:
            return self.execute_query("delete from sessions where sessions.expiration_timestamp < datetime()")
        except sqlite3.Error as e:
            print("Error delete_expired_sessions:", e)
            raise Exception("Error delete_expired_sessions")

    def delete_session_byID(self,session_id): #for logging out
        try:
            self.execute_query("delete from sessions where session_id=?", (session_id,))
            return True
        except sqlite3.Error as e:
            print("Error delete_expired_sessions:", e)
            raise Exception("Error delete_expired_sessions")

    def get_count_likes_byRecipeID(self,recipe_id):
        try:
            likes_count = self.execute_query("SELECT COUNT(*) FROM users_likes WHERE recipeId=?", (recipe_id,))
            if not likes_count: #null
                return str(0)
            return str(likes_count[0])
        except sqlite3.Error as e:
            print("Error getting likes:", e)
            raise Exception("Error getting likes")


    def get_isLiked_byUserRecipeID(self, user_id, recipe_id):
        try:
            isLiked = self.execute_query("SELECT * FROM users_likes WHERE recipeID=? AND userID=?", (recipe_id,user_id))
            if not isLiked: #null, not liked by user
                return False
            return True #liked by user
        except sqlite3.Error as e:
            print("Error getting likes:", e)
            raise Exception("Error getting likes")


    def load_reviews_byRecipeID(self,recipe_id):
        try:
            reviews = self.execute_query_all("SELECT * FROM reviews WHERE recipeId=?", (recipe_id,))
            #cursor = self.conn.cursor()
            #reviews = cursor.execute("SELECT * FROM reviews WHERE recipeId=?", (recipe_id,)).fetchall() #Fetches all rows
            if reviews: #return reviews if existed
                return reviews
            return None
        except sqlite3.Error as e:
            print("Error getting reviews:", e)
            raise Exception("Error getting reviews")


    # def get_username_by_userId(self, user_id):
    #     try:
    #         username = self.execute_query("SELECT username FROM users WHERE id = ?", (user_id,))
    #         if username[0]:
    #             return username[0]
    #         return None
    #     except sqlite3.Error as e:
    #         print("Error getting reviews:", e)
    #         raise Exception("Error getting reviews")
    #         return None

    def like_or_dislike(self,user_id, recipe_id):
        #remove or add new like to users_likes
        if self.get_isLiked_byUserRecipeID(user_id, recipe_id): #user wants to dislike- remove from table
            try:
                self.execute_query("DELETE FROM users_likes WHERE recipeID=? AND userID=?",(recipe_id,user_id))
                return "dislike"
            except sqlite3.Error as e:
                print("Error delete_expired_sessions:", e)
                raise Exception("Error delete_expired_sessions")
        # user wants to like - add to table
        self.execute_query("INSERT INTO users_likes (userID, recipeID) VALUES (?,?)",(user_id,recipe_id))
        return "like"

    def delete_user_byID(self,userID):
        try:
            self.execute_query("DELETE FROM sessions WHERE user_id=?", (userID,))
            self.execute_query("DELETE FROM reviews WHERE userID=?", (userID,))
            self.execute_query("DELETE FROM users WHERE id=?", (userID,))
            return True
        except sqlite3.Error as e:
            print("Error deleting user:", e)
            raise Exception("Error deleting user")


db_manager_instance: DatabaseManager = DatabaseManager('user_DB.db')