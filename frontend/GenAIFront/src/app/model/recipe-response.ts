export class RecipeResponse {
    recipe_name: string;
    ingredients: string[];
    recipes: string[];
    urls: string;
    constructor(){
        this.recipe_name = '';
        this.ingredients = [];
        this.recipes = [];
        this.urls = ''
    }
}