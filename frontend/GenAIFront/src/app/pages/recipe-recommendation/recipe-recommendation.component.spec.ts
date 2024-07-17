import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecipeRecommendationComponent } from './recipe-recommendation.component';

describe('RecipeRecommendationComponent', () => {
  let component: RecipeRecommendationComponent;
  let fixture: ComponentFixture<RecipeRecommendationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecipeRecommendationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecipeRecommendationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
