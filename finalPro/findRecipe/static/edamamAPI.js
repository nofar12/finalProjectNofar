const API_KEY = 'dab1922008b44fa6e74f63cb2d195999';
const API_ENDPOINT = 'https://api.edamam.com/search';
const APP_ID = 'e862c32a';

function searchRecipes(){
  const ingredient = document.getElementById('ingredientInput').value;
  const url =  'https://api.edamam.com/api/recipes/v2?q=' + ingredient + '&type=public&app_id=' + APP_ID + '&app_key=' + API_KEY;
  var table = document.getElementById('recipeTbl');
    table.innerHTML = "";
  var tr = document.createElement('tr');
  tr.innerHTML = '<tr><th>Name</th><th>Image</th></tr>';
  table.appendChild(tr);

  fetch(url) //sending request to the url
        .then(response => response.json()) //find the JSON content of the response - the recipes
        .then(data => { data.hits.forEach( (recipe) => {
            var tr = document.createElement('tr');
            tr.innerHTML = '<td>' + recipe.recipe.label + '</td>' +
            '<td><img src="' + recipe.recipe.image + '"></td>' ;
             table.appendChild(tr);
        } )})
        //searching for errors
        .catch(error => console.error('Error fetching recipes:', error.message));
}
