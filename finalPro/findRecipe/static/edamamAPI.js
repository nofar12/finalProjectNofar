const API_KEY = 'dab1922008b44fa6e74f63cb2d195999';
const API_ENDPOINT = 'https://api.edamam.com/search';
const APP_ID = 'e862c32a';


const searchRecipes = async (query) => {
  const url = `${API_ENDPOINT}?q=${query}&app_id=${APP_ID}&app_key=${API_KEY}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Failed to fetch recipes');
    }
    const data = await response.json();
    return data.hits.map(hit => hit.recipe);
  } catch (error) {
    console.error('Error fetching recipes:', error.message);
    return [];
  }
};


