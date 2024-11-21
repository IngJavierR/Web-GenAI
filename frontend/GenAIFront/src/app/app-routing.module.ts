import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ChatDocumentsComponent } from './pages/chat-documents/chat-documents.component';
import { TweetPreviewComponent } from './pages/tweet-preview/tweet-preview.component';
import { RecipeRecommendationComponent } from './pages/recipe-recommendation/recipe-recommendation.component';
import { MarketplaceComponent } from './pages/marketplace/marketplace.component';

const routes: Routes = [
  { path: 'chat', component: ChatDocumentsComponent },
  { path: 'content', component: TweetPreviewComponent },
  { path: 'recipe', component: RecipeRecommendationComponent },
  { path: 'marketplace', component: MarketplaceComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
