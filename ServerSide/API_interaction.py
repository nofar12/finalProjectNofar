import json
import urllib.request
API_KEY = 'dab1922008b44fa6e74f63cb2d195999'
APP_ID = 'e862c32a'
API_URL = 'https://api.edamam.com/api/recipes/v2'

class API_Interaction:
    @staticmethod
    def get_recipe_byID(id):
        url = API_URL+ '/' + id + '?type=public&app_id=' + APP_ID + '&app_key=' + API_KEY
        try:
             # fetching data from Edamam API
             # Send HTTP GET request to the URL and retrieve the response
             with urllib.request.urlopen(url) as response:
                 if response.getcode() == 200: # Check if the response status code is OK
                    recipe_data = json.loads(response.read().decode())
                    return recipe_data
                 return None

        except Exception as e:
             print('Error fetching recipes:', e)
             return None

    @staticmethod
    def random_recipes():
        try:
            # fetching data from Edamam API
            with urllib.request.urlopen(API_URL + '?type=public&app_id=' + APP_ID + '&app_key=' + API_KEY +'&random=true&diet=balanced') as response:
                if response.getcode() == 200:  # Check if the response status code is OK
                    recipe_data = json.loads(response.read().decode())
                    return recipe_data
                return None

        except Exception as e:
            print('Error fetching recipes:', e)
            return None

    @staticmethod
    def search(filters):
       try:
           # constructing the request format
           api_url = API_URL + '?type=public&app_id=' + APP_ID + '&app_key=' + API_KEY
           queryStr = ""
           if filters.get("q"): #if not none
               queryStr+="&q=" + urllib.parse.quote_plus(filters.get("q"))  #Replace special characters in string and replace spaces with plus signs

           caloriesFrom = filters.get("calories_from")
           caloriesTo = filters.get("calories_to")
           str_calr = API_Interaction.from_to_formatting(caloriesFrom, caloriesTo, "calories")
           if str_calr: #if not none
               queryStr += str_calr

           ingrFrom = filters.get("ingr_from")
           ingrTo = filters.get("ingr_to")
           str_ingr = API_Interaction.from_to_formatting(ingrFrom, ingrTo, "ingr")
           if str_ingr: #if not none
               queryStr += str_ingr

           totalTime = filters.get("totalTime")
           if totalTime:
               queryStr += "&time=" + totalTime

           diets = filters.get("diets") #array
           if diets and len(diets) > 0:
               for diet in diets:
                   queryStr += "&diet=" + diet.lower()

           allergies = filters.get("allergies")  # array
           if allergies and len(allergies) > 0:
               for allergy in allergies:
                   allergy = allergy.lower()
                   if allergy[-1]=="s": #check last character (plural)
                       allergy = allergy.replace(" ", "-") # for "tree nut" value - exception string - contain two words
                       allergy = allergy[:-1]+ "-free"
                   else:
                       allergy += "-free"
                   queryStr += "&health=" + allergy

           dietaryPrefer = filters.get("dietaryPrefer")  # array
           if dietaryPrefer and len(dietaryPrefer) > 0:
               for prefer in dietaryPrefer:
                   prefer = prefer.lower()
                   prefer = prefer.replace(" ", "-")
                   queryStr += "&health=" + prefer

           mealType = filters.get("mealType")
           if mealType and mealType != "All":
               queryStr += "&mealType=" + mealType

           cuisineType = filters.get("cuisineType")
           if cuisineType and cuisineType != "All":
               queryStr += "&cuisineType=" + urllib.parse.quote_plus(cuisineType)

           dishType = filters.get("dishType")
           if dishType and dishType != "All":
               queryStr += "&dishType=" + urllib.parse.quote_plus(dishType)

           excludedIngredients = filters.get("excludedIngredients") # array
           if excludedIngredients and len(excludedIngredients) > 0:
               for ingredient in excludedIngredients:
                   queryStr += "&excluded=" + ingredient.lower()


           print(api_url + queryStr)
           # fetching data from Edamam API
           with urllib.request.urlopen(api_url + queryStr) as response:
               data = json.loads(response.read().decode())
               return data

       except Exception as e:
           print('Error fetching recipes:', e)
           return None

    @staticmethod
    def from_to_formatting (min,max, parm_name):
        if min and max:
            return f"&{parm_name}=" + min + "-" + max
        elif min and not max:
            return f"&{parm_name}=" + min + "+"
        elif not min and max:
            return f"&{parm_name}=" + max
        return None





