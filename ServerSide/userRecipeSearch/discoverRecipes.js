let noValidInputFilters = ""
let filters = null    //object of the required client"s filters

let current_page = 0 //counter of the recipe page number
var recipePagesStack = [] // stack to store pages of recipes




function getRecipeID(recipeObj){
//extracting the ID of recipe which is in "uri"
//for example: http://www.edamam.com/ontologies/edamam.owl#recipe_dc5c64ba92411c751784d3e399d053ce
//the id in this case will be: dc5c64ba92411c751784d3e399d053ce
    var uri = recipeObj.recipe.uri
    var index = uri.indexOf("#recipe_")
    if (index !== -1) { // Check if "#recipe_" exists in the uri
        var recipe_id = uri.substring(index + "#recipe_".length) // Extract the ID after "#recipe_"
        return recipe_id
    }
    return null // return null if "#recipe_" is not found in the uri
}

function displayRecipes(recipes,tableElement) {
      recipes.forEach(recipe => {
        const card = document.createElement("div")
        card.className = "recipe-card"
        card.dataset.recipeId = getRecipeID(recipe) // set the recipe ID as a custom data attribute (data-id)
        card.innerHTML =  "<h4>" + recipe.recipe.label + "</h4>" + "<img src='" + recipe.recipe.image + "'>"
        card.addEventListener("click", function() {
            loadRecipePage(card.dataset.recipeId) // recipe ID stored in data-recipeId attribute
        })
        tableElement.appendChild(card)
      })
}



function randomRecipes(){
  let url =location.protocol + "://" + location.host + ":" + location.port + "/recipesAction?action=random"
  var table = document.getElementById("recipes-table")
  table.innerHTML = "" // Clear the table
  var message = document.getElementById("error-msg")
  message.innerHTML = "" // Clear the error message

  //hide the "next page" and "previous page" buttons
  document.getElementById("next-results").style.display = "none"
  document.getElementById("previous-results").style.display = "none"

  fetch(url)
    .then(response => response.json())
    .then(data => {
      const recipes = data.hits.slice(0, 9) // Limit to the first 9 recipes
      displayRecipes(recipes,table) //show the recipes on the page
    })
    .catch(error => console.error("Error fetching recipes:", error.message))
}

function searchRecipes(){
    var table = document.getElementById("recipes-table")
    table.innerHTML = "" // Clear the table
    var message = document.getElementById("error-msg")
    recipePagesStack = []
    //hide the "next page" and "previous page" buttons
    document.getElementById("next-results").style.display = "none"
    document.getElementById("previous-results").style.display = "none"
    const user_input = document.getElementById("recipeInput").value

    if  (user_input.trim()=="" &&  document.getElementById("filtersActive").querySelector("p").innerHTML == "Not active"){
        alert("Enter a search term or add filters")
        return
    }

    if(filters == null){
        filters = {}
    }

   filters.q = user_input
    // convert filters object (the user's selected filters) to JSON string
   const jsonFilters = JSON.stringify(filters)

   const url = location.protocol + "://" + location.host + ":" + location.port + "/recipesAction?action=search" // the "location" object in js contains info about the url
   fetch(url, {
       method: "POST",
       headers: {
           "Content-Type": "application/json"
       },
       body: jsonFilters
      })
      .then(response => response.json())
      .then(data => {
                if (data.count == 0) { //no results were found for the search
                   message.innerHTML = "No results found. Try searching something else!"
                }
                else {
                    message.innerHTML = "" // Clear the error message
                    const recipes = data.hits
                    recipePagesStack.push(data)  //push the current page recipes data to the stack
                    current_page = 0 // initial value
                    displayRecipes(recipes,table) //show the recipes on the page

                    if (data._links.next.href) {// if not null - define the dataset as the next page (element data-id)
                            document.getElementById("next-results").dataset.link = data._links.next.href
                            //show the "next page" button
                            document.getElementById("next-results").style.display = "flex"
                     }
                }
       })
    .catch(error => console.error("Error fetching recipes:", error.message));
}


function loadRecipesByDirection(direction) {
    var table = document.getElementById("recipes-table")
    table.innerHTML = "" // Clear the table
    var message = document.getElementById("error-msg")

    if(direction == "back"){
        current_page--
        currentData =  recipePagesStack[current_page]
        displayRecipes(currentData.hits,table)
        if(current_page ==0){ //first page
              document.getElementById("previous-results").style.display = "none"
        }

    }
    else{
        if(current_page+1 < recipePagesStack.length){
           current_page++
           currentData =  recipePagesStack[current_page]
           displayRecipes(currentData.hits,table)
           document.getElementById("previous-results").style.display = "flex"
           return
        }

        link = document.getElementById("next-results").dataset.link
        fetch(link)
        .then(response => response.json())
        .then(data => {
                            message.innerHTML = "" // Clear the error message
                            const recipes = data.hits
                            current_page++
                            recipePagesStack.push(data)
                            displayRecipes(recipes,table) //show the recipes on the page

                            if (data._links.next.href) { // if not null - define the dataset as the next page (element data-id)
                                 document.getElementById("next-results").dataset.link = data._links.next.href
                                 //recipePagesStack.push(data.hits) // push the current page recipes data to the stack
                            }else{  //no next page
                                document.getElementById("next-results").style.display = "none"
                            }

                            document.getElementById("previous-results").style.display = "flex"

                        }
          )
         .catch(error => console.error("Error fetching recipes:", error.message))

    }

}

function loadPreviousRecipes(){
    var table = document.getElementById("recipes-table")
    table.innerHTML = "" // Clear the table
    document.getElementById("error-msg").innerHTML = "" // Clear the error message

    // pop the previous page's data from the stack
    try {


        if (recipes)
            displayRecipes(recipes,table)

        current_page -= 1
        if (current_page == 0)
            document.getElementById("previous-results").style.display = "none"

        else
            document.getElementById("previous-results").style.display = "flex"
        document.getElementById("next-results").style.display = "flex"
    }
    catch (error) {
            console.error("Error loading previous recipes:", error)
    }
}



function showFiltersBar(){
    document.querySelector(".filters").style.display = "flex" //showing the filters div
    document.getElementById("filtersActive").style.display = "none" //hide selected filters div

    //hide the add filters button and show the save and close button
    document.querySelector(".filtersButton").style.display = "none"
    document.querySelector(".saveCloseButton").style.display = "block"

}
function checkboxes_selected (checkBoxes) {
    const arr =[]
    for (checkbox of checkBoxes) {
        if (checkbox.checked) {
           checkbox_label =  checkbox.labels[0]
           arr.push(checkbox_label.textContent)
        }
    }
    return arr;
}
function checkboxFilters_string(str, arr, arrName) {
   if (arr.length > 0) {
          str += arrName + ": "
          for (x of arr) {
              str += x + ","
          }
          str += "<br>"
   }
   return str
}


function inputFilters_string (str,value, valueName) {
    if (value && value.trim() !== "") { //ensures value is not null/empty string
        let regex = /^\d+$/
        if (regex.test(value)) { //check if the value contains only digits
            str += valueName + value + "<br>"
            return str
        }
        else {
            noValidInputFilters = "Please enter only numbers for " + valueName.slice(0,-2) + "."
            alert(noValidInputFilters)
            return str
        }
    }
    return str
}



function saveCloseFilters() { // show the selected filters
   filters = {}

   let str = ""
   noValidInputFilters = "" //initialize the value of the variable
   //checkbox
   const diets = checkboxes_selected(document.querySelectorAll(".diet input[type='checkbox']")) //returns array
   const allergies = checkboxes_selected(document.querySelectorAll(".allergies input[type='checkbox']")) //returns array
   const dietary = checkboxes_selected(document.querySelectorAll(".dietaryPreferences input[type='checkbox']")) //returns array

   //adding the selected checkboxes' labels to str
   str=checkboxFilters_string(str,diets,"diets")
   str=checkboxFilters_string(str,allergies,"allergies")
   str=checkboxFilters_string(str,dietary,"dietary")

    //dropdown
   const cuisine = document.getElementById("cuisineType").value
   if (cuisine != "All") {
        str += "Cuisine type: " + cuisine + "<br>"
   }
   const meal = document.getElementById("mealType").value
   if (meal != "All") {
        str += "Meal type: " + meal + "<br>"
   }
   const dish = document.getElementById("dishType").value
   if (dish != "All") {
        str += "Dish type: " + dish + "<br>"
   }

   if (userIngredients.length > 0){ //global variable from "filters.js"
        str += "Excluded ingredients:"
        for (ingredient of userIngredients) {
            let regex = /^[a-zA-Z]+$/
            if (regex.test(ingredient)) { //check if the ingredient string contains only alphabetic characters
                 str += ingredient + ","
            }
            else{
                alert("Please enter only alphabetic characters in excluded ingredients.")
                return
            }
        }
        str += "<br>"
   }
   //input
   const from_calories = document.getElementById("from-calories").value
   str = inputFilters_string(str,from_calories, "Calories-from: ")
   const to_calories = document.getElementById("to-calories").value
   str= inputFilters_string(str,to_calories , "Calories-to: ")
   const from_ingr = document.getElementById("from-ingr").value
   str = inputFilters_string(str,from_ingr, "From num of ingredients: ")
   const to_ingr = document.getElementById("to-ingr").value
   str = inputFilters_string(str,to_ingr, "Up to num of ingredients: ")
   const total_time = document.getElementById("upto-total-time").value
   str = inputFilters_string(str,total_time, "Up to total time: ")


    if (parseFloat(from_calories) >= parseFloat(to_calories) || parseFloat(from_ingr) >= parseFloat(to_ingr)) { //invalid user's input
        alert ('"To" value must be greater than "From" value.')
        return
    }

    if (noValidInputFilters != ""){ //invalid user's input
       return
    }

    if (str != "") {
        document.getElementById("filtersActive").querySelector("p").innerHTML = str

        filters = {    //update the json object of the required user's filters
            calories_from: from_calories,
            calories_to: to_calories,
            ingr_from: from_ingr,
            ingr_to: to_ingr,
            totalTime: total_time,
            diets: diets, //array
            allergies: allergies,//array
            dietaryPrefer: dietary, //array
            mealType: meal,
            cuisineType: cuisine,
            dishType: dish,
            excludedIngredients: userIngredients //array, global variable from 'filters.js'
        }
    }
    else {
        document.getElementById("filtersActive").querySelector("p").innerHTML = "Not active"
    }

    document.querySelector(".filters").style.display = "none" //showing the filters div
    document.getElementById("filtersActive").style.display = "block" //show selected filters div
    // show the add filters button and hide the save and close button
    document.querySelector(".filtersButton").style.display = "block"
    document.querySelector(".saveCloseButton").style.display = "none"
}

function loadRecipePage(recipeId) {
    console.log("Loading recipe page for ID:", recipeId)
    fetch("/view_recipe?id=" + recipeId)
        .then(response => response.text())
        .then(html => {
            const newWindow = window.open()
            newWindow.document.open()
            newWindow.document.write(html)
            newWindow.location.href='/view_recipe?id=' + recipeId
            newWindow.document.close()
        })
        .catch(error => console.error("Error loading recipe page:", error))
}





window.onload = function() {
    randomRecipes()
}