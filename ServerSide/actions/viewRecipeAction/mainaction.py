import html
import json

from ServerSide.API_interaction import API_Interaction
from urllib.parse import parse_qs
from urllib.parse import urlparse
import pkg_resources
from ServerSide.database_manager import db_manager_instance
from bs4 import BeautifulSoup
db_manager = db_manager_instance


class MainAction:
    def execute(self, HTTPReqHandler, username, userId):
        print("viewRecipeAction self.path=" + HTTPReqHandler.path)
        query_separate = parse_qs(urlparse(HTTPReqHandler.path).query)
        action = query_separate.get('action', [None])[0]
        recipe_id = query_separate.get('id', [None])[0]

        if action == "like":
            self.handleLikeAction(HTTPReqHandler, recipe_id)
            return

        if recipe_id is not None:
            recipe_html = self.recipe_page_construct(recipe_id, HTTPReqHandler)
            if recipe_html is not None:
                HTTPReqHandler.send_response(200)
                HTTPReqHandler.send_header('Content-type', 'text/html')
                HTTPReqHandler.end_headers()
                HTTPReqHandler.wfile.write(recipe_html.encode())
            else:
                HTTPReqHandler.send_response(404)
                HTTPReqHandler.end_headers()

    def handleLikeAction(self, HTTPReqHandler, recipe_id):    #Check if need to delete or add to the users_likes database
        session_id = HTTPReqHandler.get_cookieSession_id(HTTPReqHandler.headers)
        user_id = db_manager.get_userID_bySessionID(session_id)
        action =db_manager.like_or_dislike(user_id,recipe_id) #delete or add
        likeCount = db_manager.get_count_likes_byRecipeID(recipe_id)
        if action == "like":
            imageLike  = "/static/liked.png"
        else:
            imageLike =  "/static/notLiked.png"
        json_data = {"action" : action, "likeCount": likeCount, "imageLike": imageLike}
        HTTPReqHandler.send_response(200)
        HTTPReqHandler.send_header('Content-type', 'application/json')
        HTTPReqHandler.end_headers()
        HTTPReqHandler.wfile.write(json.dumps(json_data).encode())


    # construct the recipe page based on it's id (dynamically)
    def recipe_page_construct(self, recipe_id, HTTPReqHandler):
        recipe_data = API_Interaction.get_recipe_byID(recipe_id)
        if recipe_data:
            recipeObj = recipe_data.get('recipe')
            recipe_name = 'Recipe'  # backup names and image for error case
            recipe_image = '/static/no-image-available.png'
            if recipeObj is not None:
                recipe_name = recipeObj.get('label', 'Recipe')
                recipe_image = recipeObj.get('image', '/static/no-image-available.png')
                recipe_totalTime = int(recipeObj.get('totalTime'))
                if recipe_totalTime == 0:
                    recipe_totalTime = "-"
                elif recipe_totalTime // 60 > 0:
                    hours = recipe_totalTime // 60  # whole number
                    minutes = recipe_totalTime % 60  # - 60*hours
                    recipe_totalTime = f"{hours}h and {minutes}m"
                else:
                    recipe_totalTime = str(recipe_totalTime) + "m"

                recipe_cuisineType = recipeObj.get('cuisineType')[0]
                recipe_mealType = recipeObj.get('mealType')[0]
                recipe_dishType = recipeObj.get('dishType')[0]
                recipe_servings = str(recipeObj.get('yield'))
                dotPlace = recipe_servings.rfind(
                    ".")  # delete decimal dot if only 0 after  dot. For example: 4.0 ---> 4
                if dotPlace != -1:
                    if recipe_servings[dotPlace + 1:] == "0":
                        recipe_servings = recipe_servings[:dotPlace]  # num without the dot

                # count number of ingredients
                ingrList = recipeObj.get('ingredients')
                recipe_ingrNum = 0
                if len(ingrList) == 1:
                    if ingrList[1].get("text") != "string":  # ingredient exist
                        recipe_ingrNum = 1
                else:
                    for x in ingrList:
                        recipe_ingrNum += 1
                recipe_ingrNum = str(recipe_ingrNum)
                recipe_calories = str(
                    int(recipeObj.get('calories')))  # delete all decimal numbers, then convert the string
                # nutrients facts
                total_nutrients = recipeObj.get('totalNutrients')
                recipe_totalFat = str(int(total_nutrients.get('FAT').get('quantity')))
                recipe_saturatedFat = str(int(total_nutrients.get('FASAT').get('quantity')))
                recipe_transFat = str(int(total_nutrients.get('FATRN').get('quantity')))
                recipe_cholesterol = str(int(total_nutrients.get('CHOLE').get('quantity')))
                recipe_sodium = str(int(total_nutrients.get('NA').get('quantity')))
                recipe_totalCarbohydrate = str(int(total_nutrients.get('CHOCDF').get('quantity')))
                recipe_dietaryFiber = str(int(total_nutrients.get('FIBTG').get('quantity')))
                recipe_totalSugars = str(int(total_nutrients.get('SUGAR').get('quantity')))
                recipe_protein = str(int(total_nutrients.get('PROCNT').get('quantity')))
                recipe_vitaminD = str(int(total_nutrients.get('VITD').get('quantity')))
                recipe_calcium = str(int(total_nutrients.get('CA').get('quantity')))
                recipe_iron = str(int(total_nutrients.get('FE').get('quantity')))
                recipe_potassium = str(int(total_nutrients.get('K').get('quantity')))

                # nutrients facts - daily percentages calc
                total_daily = recipeObj.get('totalDaily')
                recipe_fatPrec = self.calc_percentages('FAT', total_daily)
                recipe_saturatedPrec = self.calc_percentages('FASAT', total_daily)
                recipe_cholesterolPrec = self.calc_percentages('CHOLE', total_daily)
                recipe_sodiomPrec = self.calc_percentages('NA', total_daily)
                recipe_carbohydratePrec = self.calc_percentages('CHOCDF', total_daily)
                recipe_dietaryFiberPrec = self.calc_percentages('FIBTG', total_daily)
                recipe_proteinPrec = self.calc_percentages('PROCNT', total_daily)

                recipe_vitaminDPrec = self.calc_percentages('VITD', total_daily)

                recipe_calciumPrec = self.calc_percentages('CA', total_daily)
                recipe_ironPrec = self.calc_percentages('FE', total_daily)
                recipe_potassiumPrec = self.calc_percentages('K', total_daily)

                # url to the original recipe page
                recipe_url = recipeObj.get('url')
                # ingredients
                ingredients = recipeObj.get('ingredientLines')
                recipe_ingredients = ""
                recipe_checkboxes = ""
                for ingredient in ingredients:
                    # recipe_ingredients += ingredient + "<br>"
                    recipe_checkboxes = f"<input type='checkbox' name={ingredient} value={ingredient}>"
                    recipe_ingredients += recipe_checkboxes + f"<label for={ingredient}> {ingredient}</label><br>"

                # health labels
                recipe_cautions = ""
                for caution in recipeObj.get('cautions'):
                    recipe_cautions += caution + ", "
                recipe_diets = ""
                for diet in recipeObj.get('dietLabels'):
                    recipe_diets += diet + ", "
                recipe_healthLabels = ""
                for healthLabel in recipeObj.get('healthLabels'):
                    recipe_healthLabels += healthLabel + ", "

            resource_package = __name__  # the current module
            template_file = pkg_resources.resource_filename(resource_package, 'basicRecipePage.html')  # locate the file
            replace_dic = {
                "$RECIPE_ID$": recipe_id,
                "$RECIPE_NAME$": recipe_name,
                "$RECIPE_PICTURE$": recipe_image,
                "$totalTime$": recipe_totalTime,
                "$cuisineType$": recipe_cuisineType,
                "$ingrNum$": recipe_ingrNum,
                "$mealType$": recipe_mealType,
                "$dishType$": recipe_dishType,
                "$yield$": recipe_servings,
                "$calories$": recipe_calories,
                "$FAT$": recipe_totalFat,
                "$FASAT$": recipe_saturatedFat,
                "$FATRN$": recipe_transFat,
                "$CHOLE$": recipe_cholesterol,
                "$NA$": recipe_sodium,
                "$CHOCDF$": recipe_totalCarbohydrate,
                "$FIBTG$": recipe_dietaryFiber,
                "$SUGAR$": recipe_totalSugars,
                "$PROCNT$": recipe_protein,
                "$VITD$": recipe_vitaminD,
                "$CA$": recipe_calcium,
                "$FE$": recipe_iron,
                "$K$": recipe_potassium,
                "$FAT_percentage$": recipe_fatPrec,
                "$FASAT_percentage$": recipe_saturatedPrec,
                "$CHOLE_percentage$": recipe_cholesterolPrec,
                "$NA_percentage$": recipe_sodiomPrec,
                "$CHOCDF_percentage$": recipe_carbohydratePrec,
                "$FIBTG_percentage$": recipe_dietaryFiberPrec,
                "$PROCNT_percentage$": recipe_proteinPrec,
                "$VITD_percentage$": recipe_vitaminDPrec,
                "$CA_percentage$": recipe_calciumPrec,
                "$FE_percentage$": recipe_ironPrec,
                "$K_percentage$": recipe_potassiumPrec,
                "$external_link$": recipe_url,
                "$ingredientLines$": recipe_ingredients,
                "$cautions$": recipe_cautions,
                "$dietLabels$": recipe_diets,
                "$healthLabels$": recipe_healthLabels
            }

            with open(template_file, "r", encoding="utf8") as file:
                # replacing the placeholders with the values in the dic
                # instead of writing each time: file.read().replace('$RECIPE_NAME$', recipe_name)
                updated_page = file.read()

                # get the username name by cookie
                session_id = HTTPReqHandler.get_cookieSession_id(HTTPReqHandler.headers)
                if session_id is not None:
                    print("recipe_page_construct View recipe: found sessionId=" + session_id)
                    user_rcd_dic = db_manager.get_user_detail_from_session(session_id)
                    print("Username found:", user_rcd_dic.get("username"))
                    updated_page = updated_page.replace("Loading...", user_rcd_dic.get("username"))
                    updated_page = updated_page.replace("profilePicture...", user_rcd_dic.get("profile_filename"))
                else:
                    print("recipe_page_construct: no sessionId")

                for placeholder, value in replace_dic.items():
                    updated_page = updated_page.replace(placeholder, value)

                # load total likes
                likes = db_manager.get_count_likes_byRecipeID(recipe_id)  # likes count
                updated_page = updated_page.replace("$likes_counter$", likes)  # replacing the placeholder
                # load heart image

                isLikedByUser = db_manager.get_isLiked_byUserRecipeID(user_rcd_dic.get("id"),recipe_id) #check if the recipe was liked by the user
                if isLikedByUser: #true
                    soup = BeautifulSoup(updated_page, "html.parser")# Parse the HTML content using BeautifulSoup library
                    heart_img = soup.find("img", id="heart")
                    heart_img["src"] ="/static/liked.png"
                    updated_page = str(soup)
                # load reviews
                reviews = db_manager.load_reviews_byRecipeID(recipe_id)  # list of all reviews (each review is a tuple)
                print(reviews)
                all_reviews_html = ""
                if reviews:
                    username = ""
                    userImage = ""
                    timeSent = ""
                    user_review = ""
                    for review in reviews:
                        # example for review: [(13, 'b0e9d9071a0f376b5b8e4bb0d40c1130', 'hi', None, 106, '2024-05-17 21:31:55')]
                        user_rcd = db_manager.get_user_detail(review[3])
                        if user_rcd:
                            username = user_rcd.get("username")
                            userImage = user_rcd.get("profile_filename")
                        user_review = review[2]
                        timeSent = review[4]
                        html_load_review = f'''
                                        <div class="review-card">
						                    <img src="{userImage}" alt="Profile Picture" class="profilePicture">
                                            <div class="review">
                                                <h3>{username} says:</h3>
                                                <p>{html.escape(user_review)}</p>
                                                <p class= "time">{timeSent}</p>
                                            </div>
					                    </div>
                                    '''
                        all_reviews_html += html_load_review

                updated_page = updated_page.replace('$cards$', all_reviews_html)  # adding all the reviews cards


            return updated_page
        else:
            return None



    def calc_percentages(self, valueName, total_daily_obj):
        return str(
            int(total_daily_obj.get(valueName).get('quantity')))  # The recommended percentage daily  of the value


