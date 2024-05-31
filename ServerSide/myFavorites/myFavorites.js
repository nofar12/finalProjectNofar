function loadMyFavorites(){
    const url = location.protocol + "://" + location.host + ":" + location.port + "/load_favorites"
    fetch(url, {
            method: "GET"
        }).then(response => response.json())
        .then(data => {
            var table = document.getElementById("recipes-table")
            table.innerHTML = "" // Clear the table
            displayRecipes(data,table)
        } )
}

function displayRecipes(recipes,tableElement) {
      recipes.forEach(recipe => {
        const card = document.createElement("div")
        card.className = "recipe-card"
        card.dataset.recipeId = getRecipeID(recipe) // set the recipe ID as a custom data attribute (data-id)
        card.innerHTML =  "<h4>" + recipe.label + "</h4>" + "<img src='" + recipe.image + "'>"
        card.addEventListener("click", function() {
            loadRecipePage(card.dataset.recipeId) // recipe ID stored in data-recipeId attribute
        })
        tableElement.appendChild(card)
      })
}


function getRecipeID(recipeObj){
//extracting the ID of recipe which is in "uri"
//for example: http://www.edamam.com/ontologies/edamam.owl#recipe_dc5c64ba92411c751784d3e399d053ce
//the id in this case will be: dc5c64ba92411c751784d3e399d053ce
    var uri = recipeObj.uri
    var index = uri.indexOf("#recipe_")
    if (index !== -1) { // Check if "#recipe_" exists in the uri
        var recipe_id = uri.substring(index + "#recipe_".length) // Extract the ID after "#recipe_"
        return recipe_id
    }
    return null // return null if "#recipe_" is not found in the uri
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
