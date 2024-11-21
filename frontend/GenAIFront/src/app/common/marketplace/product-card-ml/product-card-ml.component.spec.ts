import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductCardMlComponent } from './product-card-ml.component';

describe('ProductCardMlComponent', () => {
  let component: ProductCardMlComponent;
  let fixture: ComponentFixture<ProductCardMlComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProductCardMlComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductCardMlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
