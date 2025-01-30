import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTableModule } from '@angular/material/table';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChatDocumentsComponent } from './pages/chat-documents/chat-documents.component';
import { HttpClientModule } from '@angular/common/http';
import { TweetPreviewComponent } from './pages/tweet-preview/tweet-preview.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatGridListModule } from '@angular/material/grid-list';
import { RecipeRecommendationComponent } from './pages/recipe-recommendation/recipe-recommendation.component';
import { DocumentProcessingComponent } from './pages/document-processing/document-processing.component';

@NgModule({
  declarations: [
    AppComponent,
    ChatDocumentsComponent,
    TweetPreviewComponent,
    RecipeRecommendationComponent,
    DocumentProcessingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatCheckboxModule,
    MatIconModule,
    MatFormFieldModule,
    MatGridListModule,
    MatDividerModule,
    MatProgressBarModule,
    MatTableModule,
    MatSnackBarModule,
    FormsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
