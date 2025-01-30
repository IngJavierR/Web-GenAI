import { Component, OnInit } from '@angular/core';
import { RecipeResponse } from 'src/app/model/recipe-response';
import { LangChainServiceService } from 'src/app/services/lang-chain-service.service';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-recipe-recommendation',
  templateUrl: './recipe-recommendation.component.html',
  styleUrls: ['./recipe-recommendation.component.css']
})
export class RecipeRecommendationComponent implements OnInit {

  userInput: string = '';
  recipeName: string = '';
  ingredients: string[] = [];
  recipes: string[] = [];
  urls: string = ''

  constructor(
    private langService: LangChainServiceService,
    private dataService: DataService
  ) { }

  ngOnInit(): void {
  }

  sendMessage() {
    if (this.userInput.trim()) {
      this.dataService.setIsLoading(true);
      this.langService.recipeGet(this.userInput).subscribe((response: RecipeResponse) => {
        this.recipeName = response.recipe_name;
        this.ingredients = response.ingredients;
        this.recipes = response.recipes;
        this.urls = response.urls;
        this.dataService.setIsLoading(false);
      }, (error: Error) => {
        this.dataService.setIsLoading(false);
        this.dataService.setGeneralNotificationMessage(error.message);
      });
    }

  }
}
