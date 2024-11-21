import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductDetailMlComponent } from './product-detail-ml.component';

describe('ProductDetailMlComponent', () => {
  let component: ProductDetailMlComponent;
  let fixture: ComponentFixture<ProductDetailMlComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProductDetailMlComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductDetailMlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
