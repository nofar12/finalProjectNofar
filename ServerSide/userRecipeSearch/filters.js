//create html elements of the diet options
const dietOptions = ["Balanced","High-Fiber","High-Protein","Low-Carb","Low-Fat","Low-Sodium"]
const diet = document.querySelector(".diet")
dietOptions.forEach(option => {
    const checkbox_diet = document.createElement("input")
    checkbox_diet.type = "checkbox"
    checkbox_diet.value = option
    const label_diet = document.createElement("label")
    label_diet.innerHTML = option
    label_diet.appendChild(checkbox_diet)
    diet.appendChild(label_diet)
})
//create html elements of the allergies options
const allergiesOptions = ["Gluten","Dairy","Eggs","Soy","Wheat","Fish","Shellfish","Tree Nuts","Peanuts"]
const allergies = document.querySelector(".allergies")
allergiesOptions.forEach(option => {
    const checkbox_allergies = document.createElement("input")
    checkbox_allergies.type = "checkbox"
    checkbox_allergies.value = option
    const label_allergies = document.createElement("label")
    label_allergies.innerHTML = option
    label_allergies.appendChild(checkbox_allergies)
    allergies.appendChild(label_allergies)
})


//create html elements of the allergies options
const dietaryOptions = ["Vegan","Vegetarian","Low fat abs","Low Sugar","Immuno supportive","Pescatarian","Alcohol Free","Pork free","No oil added"]
const dietaryPreferences = document.querySelector(".dietaryPreferences")
dietaryOptions.forEach(option => {
    const checkbox_dietary = document.createElement("input")
    checkbox_dietary.type = "checkbox"
    checkbox_dietary.value = option
    const label_dietary = document.createElement("label")
    label_dietary.innerHTML = option
    label_dietary.appendChild(checkbox_dietary)
    dietaryPreferences.appendChild(label_dietary)
})

//create html elements of dropdown of the cuisine options
const cuisineOptions = ["All","American", "Asian", "British", "Caribbean", "Central Europe", "Chinese", "Eastern Europe", "French", "Indian", "Italian", "Japanese", "Kosher", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "South American", "South East Asian"]
const selectType_cuisine = document.getElementById("cuisineType")  // the dropdown element
cuisineOptions.forEach(option => {
    const typeOption_cuisine  = document.createElement("option")
    typeOption_cuisine.value = option
    typeOption_cuisine.innerHTML = option
    selectType_cuisine.appendChild(typeOption_cuisine)
});

//create html elements of dropdown of the meal options
const mealOptions = ["All","Breakfast", "Dinner", "Lunch", "Snack", "Teatime"]
const selectType_meal = document.getElementById("mealType")  // the dropdown element
mealOptions.forEach(option => {
    const typeOption_meal = document.createElement("option")
    typeOption_meal.value = option
    typeOption_meal.innerHTML = option
    selectType_meal.appendChild(typeOption_meal)
});

//create html elements of the dish type options
const dishOptions = ["All","Biscuits and cookies", "Bread", "Cereals", "Condiments and sauces", "Desserts", "Drinks", "Main course", "Pancake", "Preps", "Preserve", "Salad", "Sandwiches", "Side dish", "Soup", "Starter", "Sweets"]
const selectType_dish = document.getElementById("dishType")  // the dropdown element
dishOptions.forEach(option => {
    const typeOption_dish = document.createElement("option")
    typeOption_dish.value = option
    typeOption_dish.innerHTML = option
    selectType_dish.appendChild(typeOption_dish)
});



let userIngredients = [] // Array storing the excluded ingredients the user inputed
function enterIngredient(){
    let input = document.getElementById("ingredientsInput").value.trim()
    if (input !== "") {
        if (userIngredients.length == 0) { // Show the instructions
            document.getElementById("instructionMsg").style.display = "block"
        }
        userIngredients.push(input)
        showIngredient(input)
        document.getElementById("ingredientsInput").value = ""  // Clear the input
    }
}

//creating p element for each ingredient the client enter
function showIngredient(ingredient) {
     let p = document.createElement("p")
     p.className = "ingredient"
     p.innerHTML = ingredient
     document.getElementById("ingredients").appendChild(p)

     //Event listener to remove ingredient from filters if clicked
     p.addEventListener ("click" , function(){
        let index = userIngredients.indexOf(ingredient) //returns -1 if the value is not found
        if (index != -1)
            userIngredients.splice(index,1) //starting from index, deleting the first element
        p.parentNode.removeChild(p) // remove the paragraph from the html
        if (userIngredients.length == 0) { // Hide the instructions
            document.getElementById("instructionMsg").style.display = "none"
        }
     })
}