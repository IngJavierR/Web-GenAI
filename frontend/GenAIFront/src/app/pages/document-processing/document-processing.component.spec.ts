import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentProcessingComponent } from './document-processing.component';

describe('DocumentProcessingComponent', () => {
  let component: DocumentProcessingComponent;
  let fixture: ComponentFixture<DocumentProcessingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DocumentProcessingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DocumentProcessingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
